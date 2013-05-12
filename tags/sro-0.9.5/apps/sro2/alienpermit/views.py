# -*- coding: utf-8 -*-
'''
Alien permit views
'''
from sro2.shared import *

@login_required
def    alienpermit_add(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = PermitAddForm(request.POST)
        if form.is_valid():
            permit = None
            try:
                permit = AllienPermit(
                    no=form.cleaned_data['no'],
                    date=form.cleaned_data['date'],
                    protocol=form.cleaned_data['protocol'],
                    statement=form.cleaned_data['statement'],
                    orgsro=orgsro,
                    ver=form.cleaned_data['ver']
                )
                permit.save()
            except:
                transaction.rollback()
            else:
                transaction.commit()
            if permit is not None:
                __log_it(request, permit, ADDITION)
                transaction.commit()
            return redirect(orgsro_stagelist_edit,orgsro_id=orgsro.id)
    else:
        form = PermitAddForm()
    form.setdata(orgsro)
    return HttpResponse('ZOMFG!! Aliens attack!!!')
    #return render_to_response('sro2/alienpermit/alienpermit_add.html', RequestContext(request, {'orgsro': orgsro, 'form': form, 'type': 'Свидетельство'}))
