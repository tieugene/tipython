"""
reports.views
"""

# 2. django
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import redirect
from django.views.generic import ListView
# 4. my
from core.models import FileSeq, Org
from invoice.models import Approver, Payer
from invoice.views_extras import ROLE_ACCOUNTER, ROLE_ASSIGNEE, ROLE_BOSS
from invarch.models import Scan
from . import forms


class LedgerList(ListView):
    """
    "Табличка"
    TODO: Гендир, Бухгалтер, Исполнитель
    """
    template_name = 'reports/ledger_list.html'
    paginate_by = 25
    filter = {
        'payer':    None,
        'shipper':  None,
    }
    enabled_users = {ROLE_ASSIGNEE, ROLE_BOSS, ROLE_ACCOUNTER}

    def get_queryset(self):
        user = self.request.user
        self.approver = Approver.objects.get(user=user)
        role_id = self.approver.role.pk
        # 1. handle session
        self.paginate_by = self.request.session.get('ledger_lpp', 25)
        self.filter['payer'] = self.request.session.get('ledger_payer', None)
        self.filter['shipper'] = self.request.session.get('ledger_shipper', None)
        q = FileSeq.objects
        # 2. create query
        if (role_id in self.enabled_users) or user.is_superuser:
            payer = Payer.objects.get(pk=self.filter['payer']) if self.filter['payer'] else None
            shipper = Org.objects.get(pk=self.filter['shipper']) if self.filter['shipper'] else None
            if payer or shipper:
                if payer:
                    q = q.filter(Q(bill__payer=payer) | Q(scan__payer=payer.name))
                if shipper:
                    q = q.filter(Q(bill__shipper=shipper) | Q(scan__shipper=shipper))
            else:
                q = q.all()
            q = q.order_by('-pk')    # [:100]
        else:
            q = q.none()
        return q

    def get_context_data(self, **kwargs):
        context = super(LedgerList, self).get_context_data(**kwargs)
        context['ledger_lpp'] = self.paginate_by
        context['form'] = forms.FilterLedgerListForm(initial={
            'payer': self.filter['payer'],
            'shipper': self.filter['shipper'],
        })
        return context


@login_required
def ledger_set_lpp(request, lpp):
    request.session['ledger_lpp'] = int(lpp)
    return redirect('ledger_list')


@login_required
def ledger_set_filter(request):
    form = forms.FilterLedgerListForm(request.POST)
    if form.is_valid():
        filt = form.cleaned_data
        request.session['ledger_payer'] = filt['payer'].pk if filt['payer'] else None
        request.session['ledger_shipper'] = filt['shipper'].pk if filt['shipper'] else None
    return redirect('ledger_list')


class SummaryList(ListView):
    """
    "Итого"
    """
    template_name = 'reports/summary_list.html'
    filter = {
        'place':    None,
        'subject':  None,
        'year':     None,
    }
    sum = 0

    def get_queryset(self):
        self.filter['place'] = self.request.session.get('summary_place', None)
        self.filter['subject'] = self.request.session.get('summary_subject', None)
        self.filter['year'] = self.request.session.get('summary_year', None)
        # locals
        p = self.filter['place']
        s = self.filter['subject']
        y = self.filter['year']
        # let's query
        # q = Scan.objects.values('place', 'subject', 'depart').filter(place=self.filter['place'], subject=self.filter['subject'], date__year=self.filter['year']).order_by('depart').annotate(Sum('sum'))
        # q = Place.objects.all()
        q = Scan.objects
        self.sum = 0
        if p and y:
            if s:
                q = q.values('depart').filter(place=p, subject=s, date__year=y).order_by('depart').annotate(Sum('sum'))
            else:
                q = q.values('depart').filter(place=p, subject=None, date__year=y).order_by('depart').annotate(Sum('sum'))
            self.sum = q.aggregate(Sum('sum__sum')).get('sum__sum__sum', 0)
        else:
            q = q.none()
        return q

    def get_context_data(self, **kwargs):
        context = super(SummaryList, self).get_context_data(**kwargs)
        context['form'] = forms.FilterSummaryListForm(initial={
            'place':    self.filter['place'],
            'subject':  self.filter['subject'],
            'year':     self.filter['year'],
        })
        context['sum'] = self.sum
        return context


@login_required
def summary_set_filter(request):
    form = forms.FilterSummaryListForm(request.POST)
    if form.is_valid():
        filt = form.cleaned_data
        request.session['summary_place'] = filt['place'] if filt['place'] else None
        request.session['summary_subject'] = filt['subject'] if filt['subject'] else None
        request.session['summary_year'] = filt['year'] if filt['year'] else None
    return redirect('summary_list')
