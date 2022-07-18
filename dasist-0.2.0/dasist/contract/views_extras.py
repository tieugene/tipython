"""
contract.views_extras
"""

# 1. system
# 2. django
# from django.contrib.auth.models import User
from django.urls import reverse
# 3. my
from invoice.models import Approver, Role
from invoice.utils import send_mail
from invoice.views_extras import \
    ROLE_ACCOUNTER, ROLE_BOSS, ROLE_CHIEF, ROLE_SDOCHIEF, \
    STATE_ONPAY, STATE_ONWAY, STATE_REJECTED, \
    USER_BOSS, USER_LAWER, USER_SDOCHIEF
from core.models import File


def update_fileseq(file, fileseq):
    """
    @param file:django.core.files.uploadedfile.InMemoryUploadedFile
    @param fileseq:FileSeq
    """
    myfile = File(file=file)
    myfile.save()
    fileseq.add_file(myfile)


def fill_route(contract, mgr, booker):
    std_route1 = [    # role_id, approve_id
        (ROLE_SDOCHIEF, Approver.objects.get(pk=USER_SDOCHIEF)),
        (ROLE_CHIEF, mgr),
        (ROLE_BOSS, Approver.objects.get(pk=USER_BOSS)),
        (ROLE_ACCOUNTER, booker),
    ]
    for r in std_route1:
        contract.route_set.create(
            role=Role.objects.get(pk=r[0]),
            approve=r[1]
        )


def __emailto(request, emails, contract_id, subj):
    """
    Send email to recipients
    @param emails:list - list of emails:str
    @param contract_id:int
    @param subj:str - email's Subj
    """
    if emails:
        send_mail(
            emails,
            '%s: %d' % (subj, contract_id),
            request.build_absolute_uri(reverse('contract.views.contract_view', kwargs={'id': contract_id})),
        )


def mailto(request, contract):
    """
    Sends emails to applicants:
    - onway - to rpoint role or aprove
    - Accept/Reject - to assignee
    @param contract:Contract
    """
    state = contract.get_state_id()
    lawyer = Approver.objects.get(pk=USER_LAWER)
    if state == STATE_ONWAY:
        subj = 'Договор на замечания'
        emails = list()
        for i in contract.route_set.all():
            emails.append(i.approve.user.email)
        emails.append(lawyer.user.email)
        __emailto(request, emails, contract.pk, subj)
    elif state == STATE_REJECTED:
        __emailto(request, [contract.assign.user.email], contract.pk, 'Договор завернут')
    elif state == STATE_ONPAY:
        __emailto(request, [lawyer.user.email], contract.pk, 'Договор требует одобрения')
