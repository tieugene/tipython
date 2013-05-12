# -*- coding: utf-8 -*-
'''
Backup views
'''
from sro2.shared import *

@login_required
#@transaction.commit_manually
def	permit_pause(request, permit_id, danger):
	'''
	не используется !!!
	для приостановки/возобновления работ по отдельности
	Pauseing / Resuming stages

	# TODO: return commit_manually

	# OMFG=(

	* parse posted json dict: {"active":[],"paused":[],"protocol":int,"datesince":str}
	* two case:
	* * changes by same date -- write changes into exist snapshot
	* * new date -- make new snap and create new PermitStages (with changes from previous snaps)
	'''
	post=request.POST.items()
	import simplejson
	stages=simplejson.loads(str(post[0][0]))
	stagelist_old = StageList.objects.get(pk=permit_id)
	active=stages['active'] #список действующих (только id)
	paused=stages['paused'] #список приостановленных (id, date)
	protocol=int(stages['protocol'])
	protocol= Protocol.objects.get(pk=protocol)
	try:
		datesince=stages['datesince']
		datesince=datesince.split('.')
		datesince='%s-%s-%s' % (datesince[2],datesince[1],datesince[0])
	except:
		datesince=dt.today()

	try:
		if str(datesince)==str(stagelist_old.date) and protocol==stagelist_old.protocol:
			permit=stagelist_old
			for stg in active:
				stage = Stage.objects.get(id=stg['id'])
				ps=PermitStage.objects.get(stagelist=stagelist_old,stage=stage, danger=int(danger))
				ps.paused=None
				ps.save()

			for stg in paused:
				date=stg['date'].split('.')
				stage = Stage.objects.get(id=stg['id'])
				ps=PermitStage.objects.get(stagelist=stagelist_old,stage=stage, danger=int(danger))
				ps.paused='%s-%s-%s' % (date[2],date[1],date[0])
				ps.save()
		else:
			permit = Permit(
				orgsro = stagelist_old.orgsro,
				ver = stagelist_old.ver,
				no = stagelist_old.no,
				date = datesince,
				protocol = protocol,
				statement = stagelist_old.statement
				)
			permit.save()
			__log_it(request, permit, ADDITION)

			for stg in active:
				stage = Stage.objects.get(id=stg['id'])
				PermitStage(stagelist=permit, stage=stage, danger=int(danger), paused=None).save()

			for stg in paused:
				date=stg['date'].split('.')
				stage = Stage.objects.get(id=stg['id'])
				PermitStage(stagelist=permit, stage=stage, danger=int(danger), paused='%s-%s-%s' % (date[2],date[1],date[0])).save()

			if (int(danger)	== 0):
				not_danger = 1
			else:
				not_danger = 0

			for permitstage_old in stagelist_old.permitstage_set.filter(danger=not_danger):
				permitstage = PermitStage(
					stagelist=permit,
					stage=permitstage_old.stage,
					danger=not_danger,
					paused=permitstage_old.paused
				).save()
		#transaction.commit()

		return HttpResponse(permit.id)

	except Exception, e:
		return HttpResponse(e)

@login_required
def	stagelist_pausestages(request,permit_id,danger):
	'''
	Не используется!!!
	для приостановки/возобновления работ по отдельности
	Page with UI for pausing/resuming stages in permit
	'''
	stagelist = StageList.objects.get(pk=permit_id)
	prevperms=stagelist.orgsro.stagelist_set.instance_of(Permit).filter(permit__no=stagelist.no)
	prevperm=prevperms[len(prevperms)-1]
	itemlist = prevperm.permitstage_set.dict(danger)
	form=ProtocolListForm()
	form.setdata(stagelist.orgsro)
	return render_to_response('sro2/stagelist_pause.html', RequestContext(request, {
		'stagelist': stagelist,
		'prevpermit_id':prevperm.id,
		'itemlist': itemlist,
#		'form': StageListListForm(),
#		'pdfform': PDFSelectForm(),
		'canedit': checkuser(stagelist.orgsro.org, request.user),
		'canedit_orgsro': checkuser(stagelist.orgsro, request.user),
		'danger': int(danger),
		'form': form,
	}))

@login_required
def	stagelist_cmp_chain(request, fromto):
	'''
	Не используется!!!
	для приостановки/возобновления работ по отдельности
	'''
	import simplejson
	from_to=simplejson.loads(fromto)
	permit_id = from_to['from']
	dest_id = from_to['to']
	permit=Permit.objects.get(pk=permit_id)
	if permit_id>dest_id:
		start=dest_id
		end=permit_id
	else:
		start=permit_id
		end=dest_id
	history=Permit.objects.all().filter(no=permit.no).filter(id__lte=end).filter(id__gte=start)
	n=0
	changes=[]
	for p in history:
		if n<(len(history)-1):
			deleted, added, common = __cmp_stagelists(p, history[n+1])
			changes.append({'chg':common,'start':p,'end':history[n+1]})
			n+=1
	return render_to_response('sro2/stagelist_cmp_chain.html', RequestContext(request, {
		'start':history[0],
		'end': history[n],
		'history': history,
		'changes': changes
	}))