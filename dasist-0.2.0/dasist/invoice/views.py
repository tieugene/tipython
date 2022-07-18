"""
invoice.views

is_staff:
* see all of invoice
* can arch
"""

# 1. system
import decimal
import json
import logging
# 3. django
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView
# 2. my
from core.models import FileSeq, FileSeqItem
from invarch.models import Scan
from . import models, forms, utils
from .views_extras import \
    ROLE_ACCOUNTER, ROLE_ASSIGNEE, ROLE_CHIEF, ROLE_LAWYER, ROLE_BOSS, \
    STATE_DONE, STATE_DRAFT, STATE_ONPAY, STATE_ONWAY, STATE_REJECTED, \
    USER_BOSS
from .views_extras import fill_route, handle_shipper, mailto, rotate_img, set_filter_state, update_fileseq

logger = logging.getLogger(__name__)

PAGE_SIZE = 25
FSNAME = 'fstate'  # 0..3


@method_decorator(login_required, name='dispatch')
class InvoiceList(ListView):
    """
    ACL:
    - All:
    -- Исполнитель: только свои (где он - Исполнитель)
    x- Руководитель: только где он - текущий Подписант или в Истории
    -- *: все
    - Inboud:
    -- Испольнитель: только свои И без подписанта (== Черновик, Завернут, Исполнен)
    -- Директор, Бухгалтер = где роль тек. Подписанта == роль юзверя
    -- *: == тек. Подписант

    """
    template_name = 'invoice/list.html'
    paginate_by = PAGE_SIZE
    # custom:
    approver = None
    mode = None

    # fsfilter = None
    # place = None
    # shipper = None
    # payer = None

    def get_queryset(self):
        # 1. vars
        self.paginate_by = self.request.session.get('lpp', PAGE_SIZE)
        user = self.request.user
        self.approver = models.Approver.objects.get(user=user)
        role_id = self.approver.role.pk
        self.mode = int(self.request.session.get('mode', 1))
        # self.fsfilter = self.request.session.get(FSNAME, 31)    # int 0..15: dropped|done|onway|draft
        # 2. query
        q = models.Invoice.objects.all().order_by('-pk')
        if self.mode == 1:  # Everything
            if (role_id == ROLE_ASSIGNEE) and (not user.is_superuser) and (not user.is_staff):  # Исполнитель
                q = q.filter(assign=self.approver)
            # 3. filter using Filter
            # - state
            fsfilter = self.request.session.get(FSNAME, None)  # int 0..15: dropped|done|onway|draft
            if fsfilter is None:
                fsfilter = 31  # all together
                self.request.session[FSNAME] = fsfilter
            else:
                fsfilter = int(fsfilter)
            q = set_filter_state(q, fsfilter)
            form_initial = {
                'dead': bool(fsfilter & 1),
                'done': bool(fsfilter & 2),
                'onpay': bool(fsfilter & 4),
                'onway': bool(fsfilter & 8),
                'draft': bool(fsfilter & 16),
            }
            # - place
            place = int(self.request.session.get('place', 0))
            if place:
                q = q.filter(place__pk=place)
                form_initial['place'] = place
            # - subject
            subject = int(self.request.session.get('subject', 0))
            if subject:
                q = q.filter(subject__pk=subject)
                form_initial['subject'] = subject
            # - depart
            depart = int(self.request.session.get('depart', 0))
            if depart:
                q = q.filter(depart__pk=depart)
                form_initial['depart'] = depart
            # - shipper
            shipper = int(self.request.session.get('shipper', 0))
            if shipper:
                q = q.filter(shipper__pk=shipper)
                form_initial['shipper'] = shipper
            # - payer
            payer = int(self.request.session.get('payer', 0))
            if payer:
                q = q.filter(payer__pk=payer)
                form_initial['payer'] = payer
            # 5. go
            self.fsform = forms.FilterBillListForm(initial=form_initial)
        else:  # Inbound
            self.fsform = None
            if role_id == ROLE_ASSIGNEE:  # Исполнитель
                q = q.filter(assign=self.approver, rpoint=None)
            elif role_id in {ROLE_LAWYER, ROLE_BOSS, ROLE_ACCOUNTER}:  # Юрист, Бухгалтер
                q = q.filter(rpoint__role=self.approver.role)
            else:
                q = q.filter(rpoint__approve=self.approver)
        return q

    def get_context_data(self, **kwargs):
        context = super(InvocieList, self).get_context_data(**kwargs)
        context['lpp'] = self.paginate_by
        context['role'] = self.approver.role
        context['canadd'] = self.approver.canadd
        context['mode'] = self.mode
        context['fsform'] = self.fsform
        return context


def invoice_get_subjects(request):
    """
    AJAX callback on place change
    """
    place = request.GET.get('place')
    ret = [dict(id='', value='---'), ]
    if place:
        for subj in models.Subject.objects.filter(place=place).order_by('name'):
            ret.append(dict(id=subj.pk, value=subj.name))
    return HttpResponse(json.dumps(ret), content_type='application/json')


@login_required
def invoice_filter_state(request):
    """
    Set filter on state of bill list
    POST only
    * set filter in cookie
    * redirect
    ACL: *
    """
    fsform = forms.FilterBillListForm(request.POST)
    if fsform.is_valid():
        fsfilter = \
            int(fsform.cleaned_data['dead']) * 1 | \
            int(fsform.cleaned_data['done']) * 2 | \
            int(fsform.cleaned_data['onpay']) * 4 | \
            int(fsform.cleaned_data['onway']) * 8 | \
            int(fsform.cleaned_data['draft']) * 16
        request.session[FSNAME] = fsfilter
        request.session['place'] = fsform.cleaned_data['place'].pk if fsform.cleaned_data['place'] else 0
        request.session['subject'] = fsform.cleaned_data['subject'].pk if fsform.cleaned_data['subject'] else 0
        request.session['depart'] = fsform.cleaned_data['depart'].pk if fsform.cleaned_data['depart'] else 0
        request.session['shipper'] = fsform.cleaned_data['shipper'].pk if fsform.cleaned_data['shipper'] else 0
        request.session['payer'] = fsform.cleaned_data['payer'].pk if fsform.cleaned_data['payer'] else 0
    return redirect('invoice_list')


@login_required
def invoice_set_lpp(request, lpp):
    """
    Set lines-per-page of bill list.
    ACL: *
    """
    request.session['lpp'] = lpp
    return redirect('invoice_list')


@login_required
def invoice_set_mode(request, mode):
    """
    Set bill list mode (all/inbound)
    ACL: *
    """
    request.session['mode'] = mode
    return redirect('invoice_list')


@login_required
@transaction.atomic
def invoice_add(request):
    """
    Add new (draft) bill
    ACL: Исполнитель
    """
    user = request.user
    approver = models.Approver.objects.get(user=user)
    if approver.role.pk != ROLE_ASSIGNEE:
        return redirect('invoice_list')
    if request.method == 'POST':
        # path = request.POST['path']
        form = forms.BillAddForm(request.POST, request.FILES)
        if form.is_valid():
            # FIXME: add transaction
            # 1. create fileseq
            fileseq = FileSeq.objects.create()
            # 2. convert image and add to fileseq
            update_fileseq(request.FILES['file'], fileseq, form.cleaned_data['rawpdf'])
            # 3. bill at all
            shipper = handle_shipper(form)
            bill = models.Invoice.objects.create(
                fileseq=fileseq,
                place=form.cleaned_data['place'],
                subject=form.cleaned_data['subject'],
                depart=form.cleaned_data['depart'],
                payer=form.cleaned_data['payer'],
                shipper=shipper,
                billno=form.cleaned_data['doc_no'],
                billdate=form.cleaned_data['doc_date'],
                billsum=form.cleaned_data['doc_sum'],
                payedsum=form.cleaned_data['sum_payed'],
                topaysum=form.cleaned_data['sum_2pay'],
                assign=approver,
                rpoint=None,
                state=models.State.objects.get(pk=STATE_DRAFT),
            )
            # 4. add route
            # boss = form.cleaned_data['boss']
            fill_route(bill)
            return redirect('invoice_view', bill.pk)
    else:
        form = forms.BillAddForm()
    return render(request, 'invoice/form.html', {
        'form': form,
        'places': models.Place.objects.all(),
    })


@login_required
@transaction.atomic
def invoice_edit(request, pk):
    """
    Update (edit) new Draft bill
    ACL: root | (Испольнитель & Draft & !Locked)
    TODO: transaction
    """
    doc = get_object_or_404(models.Invoice, pk=int(pk))  # FIXME: select_for_update(nowait=False)
    # bill = models.Bill.objects.get(pk=int(pk))
    user = request.user
    approver = models.Approver.objects.get(pk=user.pk)
    if not (request.user.is_superuser or (
            (doc.assign == approver) and
            (doc.get_state_id() == STATE_DRAFT) and
            (not doc.locked))):
        return redirect('invoice_view', bill.pk)
    if request.method == 'POST':
        form = forms.BillEditForm(request.POST, request.FILES)
        if form.is_valid():
            # FIXME: add transaction
            shipper = handle_shipper(form)
            # 1. update bill
            doc.place = form.cleaned_data['place']
            doc.subject = form.cleaned_data['subject']
            doc.depart = form.cleaned_data['depart']
            doc.payer = form.cleaned_data['payer']
            doc.shipper = shipper
            doc.billno = form.cleaned_data['billno']
            doc.billdate = form.cleaned_data['billdate']
            doc.billsum = form.cleaned_data['billsum']
            doc.payedsum = form.cleaned_data['payedsum']
            doc.topaysum = form.cleaned_data['topaysum']
            doc.save()  # FIXME: update()
            #             2. update mgr (if required)
            #            mgr = bill.get_mgr()
            #            if (mgr.approve != form.cleaned_data['mgr']):
            #                mgr.approve = form.cleaned_data['mgr']
            #                mgr.save()
            #             2. update boss (if required)
            #            boss = bill.get_boss()
            #             if (boss.approve != form.cleaned_data['boss']):
            #                 boss.approve = form.cleaned_data['boss']
            #            if (boss.approve.pk != USER_BOSS):
            #                boss.approve = models.Approver.objects.get(pk=USER_BOSS)
            #                boss.save()
            # 3. update image
            file = request.FILES.get('file', None)
            if file:
                fileseq = doc.fileseq
                fileseq.clean_children()
                update_fileseq(file, fileseq, form.cleaned_data['rawpdf'])  # unicode error
            return redirect('invoice_view', doc.pk)
    else:  # GET
        form = forms.BillEditForm(initial={
            'id': doc.fileseq.pk,
            'place': doc.place,
            'subject': doc.subject,
            'depart': doc.depart,
            'payer': doc.payer,
            'suppinn': doc.shipper.inn,
            'suppname': doc.shipper.name,
            'suppfull': doc.shipper.fullname,
            'billno': doc.billno,
            'billdate': doc.billdate,
            'billsum': doc.billsum,
            'payedsum': doc.payedsum,
            'topaysum': doc.topaysum,
            # 'mgr':      bill.get_mgr().approve,    # костыль для initial
            # 'boss':     bill.get_boss().approve,    # костыль для initial
            # 'approver':    6,
        })
    return render(request, 'invoice/form.html', {
        'form': form,
        'object': doc,
        'places': models.Place.objects.all(),
    })


@login_required
@transaction.atomic
def invoice_reedit(request, pk):
    """
    Update (edit) locked Draft bill
    ACL: root | (Испольнитель & Draft & Locked)
    """
    doc = get_object_or_404(models.Invoice, pk=int(pk))
    # bill = models.Bill.objects.get(pk=int(pk))
    user = request.user
    approver = models.Approver.objects.get(pk=user.pk)
    if not (request.user.is_superuser or (
            (doc.assign == approver) and
            (doc.get_state_id() == STATE_DRAFT) and
            doc.locked)):
        return redirect('invoice_view', doc.pk)
    max_topaysum = doc.billsum - doc.payedsum
    if request.method == 'POST':
        form = forms.BillReEditForm(request.POST, max_topaysum=doc.billsum - doc.payedsum)
        if form.is_valid():
            # 1. update bill
            doc.topaysum = form.cleaned_data['topaysum']
            if doc.route_set.count() != 3:
                fill_route(doc)
            doc.save()
            #             2. update mgr (if required)
            #            mgr = bill.get_mgr()
            #            if (mgr.approve != form.cleaned_data['mgr']):
            #                mgr.approve = form.cleaned_data['mgr']
            #                mgr.save()
            #             2. and boss (if required)
            #            boss = bill.get_boss()
            #             if (boss.approve != form.cleaned_data['boss']):
            #                boss.approve = form.cleaned_data['boss']
            #            if (boss.approve.pk != USER_BOSS):
            #                boss.approve = models.Approver.objects.get(pk=USER_BOSS)
            #                boss.save()
            return redirect('invoice_view', doc.pk)
    else:  # GET
        # hack (fill mgr and boss for wrong invoice)
        # if (bill.route_set.count() == 0): # empty route_set
        #    mgr = models.Approver.objects.get(pk=DEFAULT_CHIEF)
        #    boss = models.Approver.objects.get(pk=DEFAULT_BOSS)
        # print "Old scheme:", bill.route_set.count()
        if doc.route_set.count() != 3:
            doc.route_set.all().delete()
            fill_route(doc)
        # /hack
        form = forms.BillReEditForm(initial={
            'topaysum': doc.topaysum if doc.topaysum else max_topaysum,
            # 'mgr':      bill.get_mgr().approve,
            # 'boss':     bill.get_boss().approve,
        })
    return render(request, 'invoice/form_reedit.html', {
        'form': form,
        'object': doc,
    })


@login_required
@transaction.atomic
def invoice_view(request, pk, upload_form=None):
    """
    TODO: use __can_resume()
    View | Accept/Reject bill
    ACL: (assignee & Draft & Route ok) | (approver & OnWay)
    - POST (Draft)
    -- Исполнитель & Draft
    -- Руководитель & Подписант онже [& Onway]
    -- Директор & Подписант.Роль егоже [& Onway]
    -- Бухгалтер & Подписант.Роль [& (Onway/Onpay)]
    -- Гендир & Подписант онже [& Onway]
    - POST (upload):
    -- user == Исполнитель & Draft
    - POST
    -- user == Исполнитель & Draft
    -- user.role == Директор | Бухгалтер == Подписант.Роль
    -- user == Подписант
    - GET
    -- root
    -- Исполнитель: user == Исполнитель
    -- Руководитель: user == Подписант или в Истории
    -- *: все
    """

    def __can_upload(bill, approver):
        """
        ACL to uppload img.
        user == bill.approver && bill.state == Draft
        """
        return (approver == bill.assign) and (bill.get_state_id() == STATE_DRAFT)

    def __upload(request, bill):
        """
        Upload file to Bill
        @param request
        @parma bill:models.Bill
        @return upload_form
        """
        upload_form = forms.BillAddFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            file = request.FILES.get('file', None)
            if file:
                fileseq = bill.fileseq
                update_fileseq(file, fileseq, upload_form.cleaned_data['rawpdf'])  # unicode error
        return upload_form

    def __can_resume(request, doc, approver):
        """
        ACL to resume.
        - Draft and user == bill assign
        - OnWay and ((user == bill.rpoint.user) or (user.role == bill.rpoint.role))
        - OnPay and user.role == Accounter
        """
        invoice_state_id = doc.get_state_id()
        return (
            request.POST['resume'] in {'accept', 'reject'} and (
                ((invoice_state_id == STATE_DRAFT) and (approver == doc.assign)) or (
                    (invoice_state_id == STATE_ONWAY) and (
                ((doc.rpoint.approve is not None) and (approver == doc.rpoint.approve)) or
                ((doc.rpoint.approve is None) and (approver.role == doc.rpoint.role))
                    )
                ) or (
                    (invoice_state_id == STATE_ONPAY) and (approver.role == doc.rpoint.role)
                )
            )
        )

    def __resume(request, doc):
        """
        @return resume_form, err[, redirect[ url]
        """
        approver = models.Approver.objects.get(user=request.user)
        invoice_state_id = doc.get_state_id()
        ok = False
        err = None
        resume_form = forms.ResumeForm(request.POST)
        if resume_form.is_valid():
            resume = (request.POST['resume'] == 'accept')
            # 0. check prerequisites
            if (not resume) and (not resume_form.cleaned_data['note']):  # resume not empty on reject
                err = 'Отказ необходимо комментировать'
            else:
                # 1. new comment
                models.Event.objects.create(
                    doc=doc,
                    approve=approver,
                    resume=resume,
                    comment=resume_form.cleaned_data['note']
                )
                # 2. update bill
                if resume:  # Ok
                    route_list = doc.route_set.all().order_by('order')
                    if invoice_state_id == STATE_DRAFT:  # 1. 1st (draft)
                        doc.rpoint = route_list[0]
                        doc.set_state_id(STATE_ONWAY)
                    elif invoice_state_id == STATE_ONWAY:  # 2. onway
                        rpoint = doc.rpoint
                        if rpoint.order == len(route_list):  # 2. last (accounter)
                            doc.set_state_id(STATE_ONPAY)
                        else:  # 3. intermediate
                            doc.rpoint = doc.route_set.get(order=rpoint.order + 1)
                    elif invoice_state_id == STATE_ONPAY:  # OnPay
                        doc.rpoint = None
                        doc.payedsum += doc.topaysum
                        doc.topaysum = decimal.Decimal('0.00')
                        doc.set_state_id(STATE_DONE)
                        doc.locked = (doc.payedsum < doc.billsum)
                else:  # Reject
                    doc.set_state_id(STATE_REJECTED)
                    doc.rpoint = None
                doc.save()
                if (doc.get_state_id() == STATE_DONE) and (doc.locked is False):  # That's all
                    doc.route_set.all().delete()
                mailto(request, doc)
                ok = True
        return ok, resume_form, err

    def __can_accept():
        pass

    def __accept():
        pass

    def __can_reject():
        pass

    def __reject():
        pass

    doc = get_object_or_404(models.Invoice, pk=int(pk))
    user = request.user
    logger.info('invoice_view: user: %s, bill: %s' % (user.username, pk))
    approver = models.Approver.objects.get(user=user)
    invoice_state_id = doc.get_state_id()
    upload_form = None
    resume_form = None
    err = ''
    if request.method == 'POST':
        if request.POST['action'] == 'upload':
            if __can_upload(doc, approver):
                upload_form = __upload(request, doc)
        else:  # resume
            if __can_resume(request, doc, approver):
                ok, resume_form, err = __resume(request, doc)
                if ok:
                    return redirect('invoice_list')
    else:  # GET
        if user.is_superuser or ((doc.assign == approver) and (invoice_state_id == STATE_DRAFT)):
            upload_form = forms.BillAddFileForm()
    if resume_form is None:
        resume_form = forms.ResumeForm()
    buttons = {
        # assignee & Draft*
        'edit': (user.is_superuser or ((doc.assign == approver) and (invoice_state_id == STATE_DRAFT))),
        # assignee & (Draft|Rejected)
        'del': (user.is_superuser or (
                    (doc.assign == approver) and (invoice_state_id in {STATE_DRAFT, STATE_REJECTED}) and (
                    doc.locked is False))
                ),
        # assignee & (Rejected*|Done?)
        'restart': (user.is_superuser or ((doc.assign == approver) and (
                (invoice_state_id == STATE_REJECTED) or ((invoice_state_id == STATE_DONE) and (doc.locked is True))))),
        # assignee & Done
        'arch': (user.is_superuser or (
                ((doc.assign == approver) or user.is_staff) and (invoice_state_id == STATE_DONE) and (
                doc.locked is False))),
    }
    # Accepting (Вперед, Согласовано, В оплате, Исполнено)
    buttons['accept'] = 0
    if invoice_state_id == STATE_DRAFT:
        if doc.assign == approver:
            buttons['accept'] = 1  # Вперед
    elif invoice_state_id == STATE_ONWAY:
        if approver.role.pk != ROLE_ACCOUNTER:
            if (((doc.rpoint.approve is None) and (doc.rpoint.role == approver.role)) or
                    ((doc.rpoint.approve is not None) and (doc.rpoint.approve == approver))):
                buttons['accept'] = 2  # Согласовано
        else:  # Accounter
            if doc.rpoint.role == approver.role:
                buttons['accept'] = 3  # В оплате
    elif invoice_state_id == STATE_ONPAY:
        if approver.role.pk == ROLE_ACCOUNTER:
            buttons['accept'] = 4  # Оплачен
    # Rejecting
    buttons['reject'] = 0
    if approver.role.pk != ROLE_ACCOUNTER:
        if (invoice_state_id == STATE_ONWAY) and (
                ((doc.rpoint.approve is None) and (doc.rpoint.role == approver.role)) or
                ((doc.rpoint.approve is not None) and (doc.rpoint.approve == approver))):
            buttons['reject'] = 1
    else:
        if (invoice_state_id in {STATE_ONWAY, STATE_ONPAY}) and (doc.rpoint.role == approver.role):
            buttons['reject'] = 1
    return render(request, 'invoice/detail.html', {
        'object': doc,
        'form': resume_form if (buttons['accept'] or buttons['reject']) else None,
        'upload_form': upload_form,
        'err': err,
        'button': buttons,
    })


@login_required
@transaction.atomic
def invoice_delete(request, pk):
    """
    Delete bill
    ACL: root | (Assignee & (Draft|Rejected) & (not Locked))
    """
    doc = get_object_or_404(models.Invoice, pk=int(pk))
    # bill = models.Bill.objects.get(pk=int(pk))
    if request.user.is_superuser or (
            (doc.assign.user.pk == request.user.pk) and
            (doc.get_state_id() in {STATE_DRAFT, STATE_REJECTED} and
             (doc.locked is False))):
        # fileseq = bill.fileseq
        doc.delete()
        # fileseq.purge()
        return redirect('invoice_list')
    return redirect('invoice_view', doc.pk)


@login_required
@transaction.atomic
def invoice_restart(request, pk):
    """
    Restart bill (partialy Done or Rejected)
    ACL: root | (Assignee & (Rejected | (Done & Locked)))
    """
    doc = get_object_or_404(models.Invoice, pk=int(pk))
    # bill = models.Bill.objects.get(pk=int(pk))
    if request.user.is_superuser or (
            (doc.assign.user.pk == request.user.pk) and
            ((doc.get_state_id() == STATE_REJECTED) or (
                    (doc.get_state_id() == STATE_DONE) and (doc.locked is True)))):
        doc.set_state_id(STATE_DRAFT)
        # hack about ols style
        if doc.route_set.count() != 3:
            doc.route_set.all().delete()
            fill_route(doc)
        # /hack
        doc.save()
    return redirect('invoice_view', doc.pk)


@login_required
def invoice_mail(request, pk):
    """
    Test of email
    @param pk: bill pk
    ACL: root only
    """
    doc = models.Invoice.objects.get(pk=int(pk))
    if request.user.is_superuser:
        utils.send_mail(
            ['ti.eugene@gmail.com'],
            'Новый счет на подпись: %s' % pk,
            'Вам на подпись поступил новый счет: %s' % request.build_absolute_uri(
                reverse('invoice_view', kwargs={'pk': doc.pk})),
        )
    return redirect('invoice_view', doc.pk)


@login_required
@transaction.atomic
def invoice_toscan(request, pk):
    """
    Move bill to scans.
    ACL: root | ((Исполнитель | is_staff) && Done && !Locked)
    """
    doc = get_object_or_404(models.Invoice, pk=int(pk))
    # bill = models.Bill.objects.get(pk=int(pk))
    if request.user.is_superuser or (
            ((doc.assign.user.pk == request.user.pk) or request.user.is_staff) and
            ((doc.get_state_id() == STATE_DONE) and (not doc.locked))):
        scan = Scan.objects.create(
            fileseq=doc.fileseq,
            place=doc.place.name,
            subject=doc.subject.name if doc.subject else None,
            depart=doc.depart.name if doc.depart else None,
            payer=doc.payer.name if doc.payer else None,
            shipper=doc.shipper,
            supplier=doc.shipper.name,
            no=doc.billno,
            date=doc.billdate,
            sum=doc.billsum,
        )
        # for event in (bill.events.all()):
        for event in (doc.event_set.all()):
            scan.event_set.create(
                approve='%s %s (%s)' % (
                    event.approve.user.last_name,
                    event.approve.user.first_name if event.approve.user.first_name else '',
                    event.approve.jobtit),
                resume=event.resume,
                ctime=event.ctime,
                comment=event.comment
            )
        doc.delete()
        return redirect('invoice_list')
    else:
        return redirect('invoice_view', doc.pk)


@login_required
def invoice_img_del(request, pk):
    """
    Delete bill img (one from).
    ACL: root | (Исполнитель && Draft)
    """
    fsi = get_object_or_404(FileSeqItem, pk=int(pk))
    fs = fsi.fileseq
    doc = fs.bill
    if request.user.is_superuser or (
            (doc.assign.user.pk == request.user.pk) and
            (doc.get_state_id() == STATE_DRAFT)):
        fs.del_file(int(pk))
    return redirect('invoice_view', fs.pk)


@login_required
# transaction.atomic
def invoice_img_up(request, pk):
    """
    Move img upper.
    ACL: root | (Исполнитель && Draft)
    """
    fsi = FileSeqItem.objects.get(pk=int(pk))
    fs = fsi.fileseq
    doc = fs.bill
    if request.user.is_superuser or (
            (doc.assign.user.pk == request.user.pk) and
            (doc.get_state_id() == STATE_DRAFT)):
        if not fsi.is_first():
            fsi.swap(fsi.order - 1)
    return redirect('invoice_view', fsi.fileseq.pk)


@login_required
# transaction.atomic
def invoice_img_dn(request, pk):
    """
    Move img lower.
    ACL: root | (Исполнитель && Draft)
    """
    fsi = FileSeqItem.objects.get(pk=int(pk))
    doc = fsi.fileseq.bill
    if request.user.is_superuser or (
            (doc.assign.user.pk == request.user.pk) and
            (doc.get_state_id() == STATE_DRAFT)):
        if not fsi.is_last():
            fsi.swap(fsi.order + 1)
    return redirect('invoice_view', fsi.fileseq.pk)


def __invoice_img_r(request, pk, folder):
    """
    Rotate image
    """
    fsi = FileSeqItem.objects.get(pk=int(pk))
    doc = fsi.fileseq.bill
    if request.user.is_superuser or (
            (doc.assign.user.pk == request.user.pk) and
            (doc.get_state_id() == STATE_DRAFT)):
        rotate_img(fsi.file, dir)
    return redirect('invoice_view', fsi.fileseq.pk)


@login_required
def invoice_img_rl(request, pk):
    """
    Rotate img left
    """
    return __invoice_img_r(request, pk, False)


@login_required
def invoice_img_rr(request, pk):
    """
    Rotate img right
    """
    return __invoice_img_r(request, pk, True)
