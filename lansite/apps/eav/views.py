# -*- coding: utf-8 -*-
'''
lansite.apps.task.views
'''

# 1. django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render_to_response, redirect
from django.template import   RequestContext
# generic views
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

# 2. python
from datetime import  date

# 4. siblings
from forms import *
#from apps.tagged.forms import ObjectListForm
import simplejson

@login_required
def	index(request):
	return direct_to_template(request, 'eav/index.html')

@login_required
def	entity_list(request):
	'''
	former index
	'''
	tos=TaggedObject.objects.all()
	for to in tos:
		to.dict=str(to.__dict__)
	return render_to_response('eav/entity_list.html', context_instance=RequestContext(request, {'tos':tos}))
	return	object_list (
		request,
		queryset = File.objects.all(),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'file/file_list.html',
		extra_context = {
			'form': FileAddForm(),
		}
	)

@login_required
def	entity_add(request):
	'''
	former eav_add
	'''
	if request.method == 'POST':
		form = TaggedObjectForm(request.POST)
		if form.is_valid():
		    item = form.save(commit=False)
		    item.save()
		    return redirect(entity_edit,item_id=item.object.id)
		return HttpResponse('form invalid')
	else:
		form=TaggedObjectForm()
	return render_to_response('eav/entity_add.html', context_instance=RequestContext(request, {'form':form}))

@login_required
def	entity_add_instant(request,obj_id,type_id):
	'''
	former eav_add_instant
	'''
	item=TaggedObject(object=Object.objects.get(pk=obj_id),tot=TaggedObjectType.objects.get(pk=type_id))
	item.save()
	return redirect(entity_edit,item_id=obj_id)

@login_required
def	eav_get_tags(to):
	tags=TaggedObjectTagType.objects.filter(tot=to.tot)
	tags2=[]
	for t in tags:
		try:
		    tt=TaggedObjectTag.objects.filter(type=t,object=to)
		    for ttt in tt:
			tags2.append({'type':t,'tag':tag_typecast(ttt)})
		except Exception,e:
		    return e
	return tags2

@login_required
def tag_typecast(tag):
    before=after=tag.value
    try:
        type=tag.type.type_class()
        if type=='str':
            pass
        elif type=='bool':
            if before:
                after=True
            else:
                after=False
        elif type=='int':
                after=int(before)
        elif type=='date':
            d,m,y = before.split('.')
            after=date(int(y), int(m), int(d))
        elif type=='object':
            form=ObjectListForm(initial={'object':before})
            ctype=ContentType.objects.get(id=tag.type.options)
            model=ctype.model_class()
            objs=model.objects.all()
            form.fields['object'].queryset = objs
            tag.form=form
        tag.value=after
    except:
        tag.value='type error'
    return tag

@login_required
def	entity_detail(request, item_id):
	'''
	former eav_detail
	'''
	obj=Object.objects.get(pk=item_id)
	to=TaggedObject.objects.get(object=obj)
	tags2=eav_get_tags(to)
	return render_to_response('eav/entity_detail.html', context_instance=RequestContext(request, {'to':to,'tags':tags2}))

	return	object_detail (
		request,
		queryset = File.objects.all(),
		object_id = object_id,
		template_name = 'file/file_detail.html',
	)

@login_required
def    entity_edit(request, object_id):
    '''
    former eav_edit
    '''
    obj=Object.objects.get(pk=object_id)
    to=TaggedObject.objects.get(object=obj)
    tags=TaggedObjectTagType.objects.filter(tot=to.tot)
    tags2=eav_get_tags(to)
    for tag in tags2:
        if tag['type'].multiplicity in [0,1]:
            tags=tags.exclude(pk=tag['type'].id)
    for type in tags:
        if type.multiplicity == 1:
            type.required=True
        elif type.multiplicity == 2:
            type.required=True
            for tag in tags2:
                if type==tag['type']:
                    type.required=False
                    break
    if request.method == 'POST':
        try:
            post=request.POST.items()
            ts=simplejson.loads(str(post[0][0].encode('utf-8')),'utf8')
            for tag in ts:
#                totag=to.tags.get(pk=int(tag['id']))
                tt=TaggedObjectTag.objects.get(object_ptr=tag['id'])
                if tag['value']=='uncheck':
                    tt.value=''
                else:
                    tt.value=tag['value']
                tt.save()
            return HttpResponse('Success')
        except Exception,e:
            return HttpResponse(e)
    else:
        return render_to_response('eav/entity_detail.html', context_instance=RequestContext(request, {'to':to,'tags':tags2, 'edit':True, 'tags_all':tags}))

@login_required
def	entity_del(request, object_id):
	'''
	former eav_del
	'''
	obj=Object.objects.get(pk=object_id)
	to=TaggedObject.objects.get(object=obj)
	to.delete()
	return redirect(entity_list)

@login_required
def    eav_get_input(request, item_id):
    tag=TaggedObjectTagType.objects.get(pk=item_id)
    if tag.type_class()=='object':
        form=ObjectListForm()
        try:
            ctype=ContentType.objects.get(id=tag.options)
        except:
            ctype=ContentType.objects.get(id=tag.options,app_label='gw')
        model=ctype.model_class()
        objs=model.objects.all()
        form.fields['object'].queryset = objs
        return HttpResponse(form)
    else:
        return HttpResponse(tag.get_control())

@login_required
def	value_add(request, item_id):
	'''
	former eav_edit_newtag
	'''
	obj=Object.objects.get(pk=item_id)
	to=TaggedObject.objects.get(object=obj)
	post=request.POST.items()
	ts=simplejson.loads(str(post[0][0].encode('utf-8')),'utf8')
	type=TaggedObjectTagType.objects.get(id=ts['type'])
	ttt = TaggedObjectTag(object=to, type=type, value=ts['value'])
	ttt.save()
	return HttpResponse('success')

@login_required
def    value_del(request, item_id, tag_id):
	'''
	former eav_edit_deltag
	'''
#    obj=Object.objects.get(pk=item_id)
#    to=TaggedObject.objects.get(object=obj)
	tag=TaggedObjectTag.objects.get(object_ptr=tag_id)
	tag.delete()
	return redirect(entity_edit,item_id=item_id)

@login_required
def    	entitytype_add(request):
	'''
	former eav_objtype_add
	'''
	types=TaggedObjectTagType.objects.all()
	if request.method == 'POST':
		form = ObjTypeForm(request.POST)
		if form.is_valid():
		    item = form.save()
		    return redirect(eav_tagtype_add)
		return HttpResponse('form invalid')
	else:
		form=TagTypeForm()
		oform=ObjTypeForm()
	return render_to_response('eav/eav_tagtype_add.html', context_instance=RequestContext(request, {'form':form, 'types':types,'oform':oform}))

@login_required
def    attribute_add(request):
    '''
    former eav_tagtype_add
    '''
    types=TaggedObjectTagType.objects.all()
#    ctypes=ContentType.objects.all()
    cform=ContentTypeListForm()
    if request.method == 'POST':
        form = TagTypeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['type']=='4':
#                return HttpResponse(form.cleaned_data['options'])
                if form.cleaned_data['options']:
                    item = form.save()
                else:
                    return HttpResponse('invalid object id')
            else:
                item = form.save()
            return redirect(eav_tagtype_add)
        return HttpResponse('form invalid')
    else:
        form=TagTypeForm()
        oform=ObjTypeForm()

    return render_to_response('eav/eav_tagtype_add.html', context_instance=RequestContext(request, {'form':form, 'types':types,'oform':oform,'cform':cform}))

@login_required
def	attribute_del(request, object_id):
	'''
	former eav_deltagtype
	'''
	type=TaggedObjectTagType.objects.get(pk=tagtype_id)
	tot=type.tot
	type.delete()
	if TaggedObjectTagType.objects.filter(tot=tot).count() == 0:
		tot.delete()
	return redirect(eav_tagtype_add)

@login_required
def eav_ctype(request):
    objs=''
    if request.method == 'POST':
        form = ContentTypeListForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['type'].id
#            return redirect(eav_tagtype_add)
            objs=ctype_get(item)
#        return HttpResponse('form invalid')
    else:
        form=ContentTypeListForm()
    return render_to_response('eav/ctype.html', context_instance=RequestContext(request, {'form':form,'objs':objs}))

@login_required
def ctype_get(ctype_id):
	ctype=ContentType.objects.get(pk=ctype_id)
	model=ctype.model_class()
	objs=model.objects.all()
	return objs

@login_required
def get_tagged(model):
    list=model.objects.all()
    tos=TaggedObject.objects.all()
    ids=[]
    for to in tos:
        ids.append(to.object.id)
    list=list.filter(id__in=ids)
    ids2=[]
    for item in list:
        ids2.append(item.id)
    list.ids=ids2
    return list

@login_required
def eav_attach(request,item_id):
    obj=Object.objects.get(pk=item_id)
    if request.method == 'POST':
        if obj not in get_tagged(Object):
            item=TaggedObject(object=obj,tot=TaggedObjectType.objects.get(name='Контакт'))
            item.save()
        to=TaggedObject.objects.get(object=obj)
        tagtype=TaggedObjectTagType.objects.get(pk=request.POST['type'])
        tag=TaggedObjectTag(object=to,type=tagtype,value=request.POST['object'])
        tag.save()
        return HttpResponseRedirect(obj.get_absolute_url())
    else:
        form=TagTypeListForm()
        fc=ContentType.objects.get(name='Файл')
        if obj not in get_tagged(Object):
            tot=TaggedObjectType.objects.get(name='Контакт')
        else:
            to=TaggedObject.objects.get(object=obj)
            tot=to.tot
        form.fields['type'].queryset = TaggedObjectTagType.objects.filter(options=fc.id,tot=tot)
        oform=ObjectListForm()
        oform.fields['object'].queryset = File.objects.all()
        return render_to_response('eav/attach_file.html', context_instance=RequestContext(request, {'form':form,'oform':oform}))

@login_required
def eav_search(request):
    if request.method == 'POST':
        post=request.POST.items()
        ts=simplejson.loads(str(post[0][0].encode('utf-8')),'utf8')
        tags=[]
        for tag in ts:
            tts=TaggedObjectTag.objects.filter(type__id=tag['type'],value=tag['value'])
            for t in tts:
                tags.append(t)

        tos=TaggedObject.objects.all()
        result=[]
        for to in tos:
            tag_set=eav_get_tags(to)
            for tag in tags:
                if {'tag':tag,'type':tag.type} in tag_set:
                    result.append(to)
        c={}
        for to in set(result):
            c[to]=0
        for to in result:
            c[to]+=1
        result=[]
        for (to,count) in c.iteritems():
            if count>=len(ts):
                result.append(to)

        return render_to_response('eav/eav_search_result.html', context_instance=RequestContext(request, {'result':result,'tags':tags,'c':c}))
    else:
        toform=TypeListForm()
        tags_all=TaggedObjectTagType.objects.all()
        return render_to_response('eav/eav_search.html', context_instance=RequestContext(request, {'toform':toform,'tags_all':tags_all}))

@login_required
def eav_upload(request):
    tots=['Свидетельство о членстве','Заключение','Заявление о внесении изменений в Свидетельство','Сертификат соответствия','Заявление о приеме в члены','Свидетельство о допуск','Письмо об отсутствии чужого свидетельства о допуске','Расписка','Лицензия на строительство','Решение о вступлении в СРО','Учредительный договор','Решение о создании предприятия','Документ, подтверждающий полномочия руководителя предприятия','Устав','Свидетельство о госрегистрации','Уведомление ФСГС','Свидетельство о постановке на учет в налоговой','Свидетельство о внесении записи в ЕГРЮЛ','Выписка из ЕГРЮЛ','Полис страхования','Договор страхования','Платежка','Допсоглашение к договору страхования','Сведения о наличии зданий, сооружений, иной недвижимости','Сведения о наличии машин, механизмов, оборудования, инвентаря и приборов','Диплом','Трудовая книжка','Приказ о приеме работника на работу','Сведения об образовании','Договор возмездного оказания услуг','Свидетельство о повышении квалификации','Свидетельство о прохождении обучения','Аттестат','Письмо об отсутствии аффилированности','Бухгалтерский баланс','Отчет о прибылях и убытках','Доверенность','Выписка из протокола','Изменения в устав','Информационное письмо','Опись','Другой документ']
    for tot in tots:
        try:
            TaggedObjectType(name=tot).save()
        except:
            pass
    return HttpResponse('Done')
