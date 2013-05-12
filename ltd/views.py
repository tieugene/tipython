# -*- coding: utf-8 -*-
'''
TODO: python-wkhtmltopdf (git://github.com/qoda/python-wkhtmltopdf.git)
'''

import json, os, sys, tempfile, time, pprint, datetime, re
from subprocess import Popen, PIPE

# 1. django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

# 2. 3rd party
#import cStringIO as StringIO
#import xhtml2pdf.pisa as pisa
from cgi import escape
#from trml2pdf import trml2pdf
#import webodt
#from webodt.converters import converter
import wkhtmltopdf, pytils

# 3. own
from apps.models import *
#from forms import *
import forms

reload(sys)
sys.setdefaultencoding("utf-8")

PAGE_SIZE = 20

#@login_required
#@superuser_only
#@render_to('gw/permission_table.html')

mnames = (
	'термидора',
	'января',
	'февраля',
	'марта',
	'апреля',
	'мая',
	'июня',
	'июля',
	'августа',
	'сентября',
	'октября',
	'ноября',
	'декабря',
)

if (len(forms.form) == 0):
	forms.genform()

def	index(request):
    return direct_to_template(request, 'index.html')

def	about(request):
    return direct_to_template(request, 'about.html')

def	doctype_index(request):
        return  object_list (
                request,
                queryset = DocType.objects.all(),
                paginate_by = PAGE_SIZE,
                page = int(request.GET.get('page', '1')),
                template_name = 'doctype_list.html',
        )

def	doctype_detail(request, item_id):
        return  object_detail (
                request,
                queryset = DocType.objects.all(),
                object_id = item_id,
                template_name = 'doctype_detail.html', # FIXME: 
        )

def	doc_del(request, item_id):
    item = DocEntity.objects.get(pk=item_id)
    type_id = item.type.pk
    item.delete()
    return redirect('views.doctype_detail', type_id)

def	__split_d(context_dict, fname, dname, mname, yname):
    '''
    Split date into day. monthname and year
    @return None
    '''
    d = datetime.datetime.strptime(context_dict[fname], '%d.%m.%Y').date()
    context_dict.update({dname: d.day, mname: mnames[d.month], yname: d.year - 2000,})

def	__split_d_to6(context_dict, key, newkey):
    '''
    Split date into six numbers
    @return None
    '''
    d = datetime.datetime.strptime(context_dict[key], '%d.%m.%Y').date()
    day = str(d.day).zfill(2)
    month = str(d.month).zfill(2)
    year = str(d.year)
    context_dict.update({
        newkey+'00': day[0],
        newkey+'01':day[1],
        newkey+'02': month[0],
        newkey+'03': month[1],
        newkey+'04': year[0],
        newkey+'05': year[1],
        newkey+'06': year[2],
        newkey+'07': year[3],
    })

def	__split_s(d, f, p, l=0):
    '''
    Split s to fieldname: char to c_dict (e.g. {'f0100': 'a', 'f0101': 'b', ...}
    @param d:dict - dict to add chars to
    @param f:str - fieldname of string to split into chars
    @param p:str - filename prefix (like 'f01')
    @return None
    FIXME: len
    '''

    if f in d:
        string = d[f]
        if l > 0:
            string = string.zfill(l)

        for i, c in enumerate(string):
            d.update({'%s%02d' % (p, i): c})

def	__split_name(context_dict, key, limit=40, count=4):

    name = context_dict[key]
    for j in range(1,count+1):
        i = limit
        if len(name) < limit:
            context_dict.update({'%s%d' % (key,j): name})
            return j
        while name[i] != ' ':
            i -= 1
        context_dict.update({'%s%d' % (key,j): name[:i]})
        name = name[i+1:]
    return j

# doctype specific functions:
def	__pre_save_auto(form):
	'''
	Prepare data for saving:
	- serialize dates
	@param form:django.forms
	@return dict
	'''
	for k, v in form.cleaned_data.items():
		if isinstance(v, datetime.date):
			form.cleaned_data[k] = v.strftime('%d.%m.%Y') if v else ''
	return form.cleaned_data['name']

def	__post_load_auto(data):
	'''
	Prepare data after loading:
	- deserialize dates
	@param data:dict
	@return dict
	'''
	p = re.compile('^\d{2}[.]\d{2}[.]\d{4}$')
	for k, v in data.items():
		if ((isinstance(v, basestring)) and (p.match(v))):
			data[k] = (datetime.datetime.strptime(v, '%d.%m.%Y').date())
	return data

# __pe_*: prepare context dict befor export
def	__pe_0001(context_dict):
    __split_d(context_dict, 'date0', 'd0', 'm0', 'y0')
    __split_d(context_dict, 'date1', 'd1', 'm1', 'y1')

def	__pe_0003(context_dict):
    __split_d_to6(context_dict, 'date0', 'f19')
    __split_d_to6(context_dict, 'date1', 'f17')
    __split_s(context_dict, 'oinn', 'f01')
    __split_s(context_dict, 'okpp', 'f02')
    __split_s(context_dict, 'kno', 'f03')
    parts = __split_name(context_dict, 'oname')
    for j in range(1,parts+1):
        __split_s(context_dict, 'oname'+str(j), 'f0' + str(j+3))
    __split_s(context_dict, 'oogrn', 'f08')
    #__split_s(context_dict, 'oogrnip', 'f09')
    #__split_s(context_dict, 'kio', 'f10')
    context_dict.update({'f11': int(context_dict['opening'])})
    __split_s(context_dict, 'bossf', 'f12')
    __split_s(context_dict, 'bossi', 'f13')
    __split_s(context_dict, 'bosso', 'f14')
    __split_s(context_dict, 'bossinn', 'f15')
    __split_s(context_dict, 'bossphone', 'f16')
    __split_s(context_dict, 'rs', 'f18')
    parts = __split_name(context_dict, 'bname')
    for j in range(1,parts+1):
        __split_s(context_dict, 'bname'+str(j), 'f2' + str(j-1))
    __split_s(context_dict, 'bzip', 'f24')
    __split_s(context_dict, 'breg', 'f25', 2)
    __split_s(context_dict, 'binn', 'f33')
    __split_s(context_dict, 'bkpp', 'f34')
    __split_s(context_dict, 'bik', 'f35')
    __split_s(context_dict, 'badistr', 'f26')
    __split_s(context_dict, 'batown', 'f27')
    __split_s(context_dict, 'bapunkt', 'f28')
    __split_s(context_dict, 'bastreet', 'f29')
    __split_s(context_dict, 'bahouse', 'f30')
    __split_s(context_dict, 'bastr', 'f31')
    __split_s(context_dict, 'baoff', 'f32')

def	__pe_0004(context_dict):
	'''
	Convert org_ocved_XX_x into list of dicts
	TODO:
		* x10
		* pagebreaks
	FIXME: и/или
	Note: костыль на костыле блин...
	'''
	# 1. OKVEDs
	okveds = list()
	thatsall = False	# indicates that list is finished
	for i in xrange(20):
		pagebreak = ((i % 10) == 0)	# break each 10 lines
		if (thatsall):
			if (pagebreak):
				break
			else:
				okveds.append(('', '', pagebreak))
				continue
		k = v = ''
		c = 'org_okved_%02d_' % i
		kname = c + 'k'
		if (context_dict.has_key(kname)):
			k = context_dict[kname]
			del context_dict[kname]
		vname = c + 'v'
		if (context_dict.has_key(vname)):
			v = context_dict[vname]
			del context_dict[vname]
		if (k and v):
			#print k, ':', v
			okveds.append((k, v, pagebreak))
		else:
			okveds.append(('', '', pagebreak))
			thatsall = True
	context_dict['org_okved'] = okveds
	# 2. Shortcuts
	# 2.1. org_Xname
	context_dict['org_fname'] = context_dict['org_fokopf'] + " " + context_dict['org_name']
	context_dict['org_sname'] = context_dict['org_sokopf'] + " " + context_dict['org_name']
	context_dict['founder_ffio'] = context_dict['founder_f'] + " " + context_dict['founder_i'] + " " + context_dict['founder_o']
	context_dict['founder_sfio'] = context_dict['founder_f'] + " " + context_dict['founder_i'][0] + ". " + context_dict['founder_o'][0] + "."
	# 2.2. founder_doc
	context_dict['founder_doc'] = "паспорт серия " + context_dict['founder_doc_series'] + " № " + context_dict['founder_doc_no'] + ", выдан " + pytils.dt.ru_strftime(u"%d %B %Y", context_dict['founder_doc_date'], inflected=True) + " года " + context_dict['founder_doc_who'] + ", код подразделения " + context_dict['founder_doc_kp']
	# 2.3. founder_addr
	context_dict['founder_addr'] = "Российская Федерация, " + context_dict['founder_addr_zip'] + ", " + context_dict['founder_addr_city'] + ", " + context_dict['founder_addr_street'] + ", " + context_dict['org_addr_building_type'] + " " + context_dict['founder_addr_building'] + ", " + context_dict['founder_addr_housing_type'] + " " + context_dict['founder_addr_housing'] + ", " + context_dict['founder_addr_office_type'] + " " + context_dict['founder_addr_office']
	# 2.4. org_addr
	context_dict['org_addr'] = "Российская Федерация, " + context_dict['org_addr_zip'] + ", " + context_dict['org_addr_city'] + ", " + context_dict['org_addr_street'] + ", " + context_dict['org_addr_building_type'] + " " + context_dict['org_addr_building'] + ", " + context_dict['org_addr_housing_type'] + " " + context_dict['org_addr_housing'] + ", " + context_dict['org_addr_office_type'] + " " + context_dict['org_addr_office']
	# 3. org_dov_fms
	context_dict['org_dov_fns'] = context_dict['org_dov_fns'].split('\n')
	context_dict['org_dov_pf'] = context_dict['org_dov_pf'].split('\n')
	context_dict['org_dov_pf_short'] = list()
	for i in context_dict['org_dov_pf']:
		fio = i.split(' ')[:3]
		#pprint.pprint(fio)
		context_dict['org_dov_pf_short'].append(fio[0] + ' ' + fio[1][0] + '. ' + fio[2][0] + '.')

def	doc_export_0004(request, item, context_dict):
        # 2. render: need request, item, context_dict
	doc = request.POST['doc']	# 0..E (string)
	tplname = 'doc_0004_%s' % doc
	if (request.POST['import'] == 'html'):	# html/pdf
		return render_to_response(tplname + '.xhtml', context_instance = Context(context_dict))
	else:
		tmp = tempfile.NamedTemporaryFile(suffix='.xhtml', delete=True)		# delete=False to debug
		tmp.write(render(request, tplname + '.xhtml', context_instance=Context(context_dict), content_type='text/xml').content)
		tmp.flush()
		outfile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=True)	# delete=False to debug
		kwargs = {'dpi': 300, 'page_footer': '"[page]"' }
		if (doc == '2'):	# Устав
			kwargs['footer_right'] =  '"[page]"'
		if (doc == 'C'):	# Список участников
			kwargs['orientation'] =  'Landscape'
		wkh = wkhtmltopdf.WKhtmlToPdf(tmp.name, outfile.name, **kwargs)
		wkh.render()
		response = HttpResponse(content=outfile.read(), mimetype='application/pdf', content_type = 'application/pdf')
		response['Content-Transfer-Encoding'] = 'binary'
		response['Content-Disposition'] = (u'attachment; filename=\"%s.pdf\";' % tplname)
		return response

dtlist = (	# pe - pre_export, ps - pre_save, pl - post_load, dt - detail template, dg - detail view GET, dp - detail view POST
	{ 'pe': __pe_0001, },
	{ 'pe': __pe_0001, },
	{ 'pe': __pe_0003, },
	{ 'pe': __pe_0004, 'dt': 'doc_detail_0004.html', 'dp': doc_export_0004},
)

def	doc_add(request, item_id):
    '''
    Extend: item prepare from form, form name
    '''
    doctype = DocType.objects.get(pk=int(item_id))
    dtid = int(doctype.pk)	# doctype id
    #e = dtlist[doctype.pk - 1]
    if request.method == 'POST':
        form = forms.DynaForm(request.POST, fieldlist=forms.formdata[dtid-1][0])
        if form.is_valid():
            name = __pre_save_auto(form)	# FIXME: ask dtlist
            item = DocEntity(type=doctype, name=name, data=json.dumps(form.cleaned_data, indent=1, ensure_ascii=False))
            item.save()
            return redirect(doctype_detail, item_id=doctype.pk)
        #return HttpResponse('form invalid')
    else:
        form = forms.DynaForm(fieldlist=forms.formdata[dtid-1][0])
    return render_to_response('doc_form_auto.html', context_instance=RequestContext(request, {'doctype': doctype, 'form':form}))

def	doc_edit(request, item_id):
    '''
    Extend: form name, data prepare befor save
    '''
    item = DocEntity.objects.get(pk=int(item_id))
    dtid = int(item.type.pk)
    #e = dtlist[item.type.pk - 1]
    if request.method == 'POST':
        form = forms.DynaForm(request.POST, fieldlist=forms.formdata[dtid-1][0])
        if form.is_valid():
            item.name = __pre_save_auto(form)	# FIXME: ask dtlist
            item.data = json.dumps(form.cleaned_data, indent=1, ensure_ascii=False)
            item.save()
            return redirect(doc_detail, item_id=item.id)
        #return HttpResponse('form invalid')
    else:	# GET
        data = __post_load_auto(json.loads(item.data))
        form = forms.DynaForm(data, fieldlist=forms.formdata[dtid-1][0])
    return render_to_response('doc_form_auto.html', context_instance=RequestContext(request, {'form': form, 'doctype': item.type}))

def	__render_odf(request, item, context_dict):
	'''
	Render fod? file to given format using LibreOffice [via unoconv]
	@param request: clearly
	@param item:DocType(?)
	@param context_dict:
	@return HttpResponse
	'''
        # 2. render: need request, item, context_dict
        export = ODFExport.objects.get(pk=int(request.POST['import']))
        tmp = tempfile.NamedTemporaryFile(suffix='.'+item.type.odftype.ext, delete=True)	# delete=False to debug
        tmp.write(render(request, 'doc_%04d.%s' % (item.type.pk, item.type.odftype.ext), context_instance=Context(context_dict), content_type='text/xml').content)
        tmp.flush()
	#print tmp.name
        # 3. convert (via webodt | libreofficed)
        #outfile = converter().convert(webodt.ODFDocument(tmp.name), format=export.ext, delete_on_close=True)
	# 3. convert (via unoconv)
	outfile = tempfile.NamedTemporaryFile(suffix='.'+export.ext, delete=True)		# delete=False to debug
	# костыль на костыле, блиа...
	if (item.type.odftype.ext == 'xhtml'):
		#wkhtmltopdf(url=""tmp.name, output_file=outfile.name)
		#wkhtmltopdf.wkhtmltopdf(url='http://www.google.com', output_file=outfile.name)
		wkh = wkhtmltopdf.WKhtmlToPdf(tmp.name, outfile.name)
		wkh.render()
	else:
		command = 'unoconv -f %s -o %s %s' % (export.ext, outfile.name, tmp.name)
		try:
			p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
			stdout, stderr = p.communicate()
			retcode = p.returncode
			if retcode < 0:
				raise Exception('terminated by signal: ', -retcode)
			elif retcode > 0:
				raise Exception(stderr)
			else:	# 0 == ok
				pass
		except OSError, exc:
			raise exc
        # 4. response (err: response = HttpResponse('We had some errors:<pre>%s</pre>' % escape(err)) )
        response = HttpResponse(content=outfile.read(), mimetype=export.mime, content_type = export.mime)
        response['Content-Transfer-Encoding'] = 'binary'
        response['Content-Disposition'] = (u'attachment; filename=\"%04d.%s\";' % (item.pk, export.ext,))
	#if (os.path.exists(outfile.name)):
	#	os.remove(outfile.name)	# hack
        return response

def	doc_detail(request, item_id):
    '''
    Extend: context prepare befor render
    TODO: dynamic:
	list(dict(); "k": "v")
	for i in data:
	
    '''
    item = DocEntity.objects.get(pk=item_id)
    if request.method == 'GET':
	keys = forms.formdata[item.type.pk - 1][0]	# SortedDict
	values = __post_load_auto(json.loads(item.data))
	data = list()
	for k in keys:
		data.append({'k': k, 'l': keys[k]['a']['label'], 'v': values.get(k, None)})
	#print 'Data:'
	#pprint.pprint(data)
	tpl = dtlist[item.type.pk - 1].get('dt', 'doc_detail_auto.html')
	return render_to_response(
		tpl,
		context_instance=RequestContext(
			request,
			{
				'object': item,
				'data': data,
			}
		)
	)
    else:	# POST == import
        # http://satels.blogspot.com/2011/06/doc-pdf-odt-html-django.html
        # OOo daemon: soffice '-accept=socket,host=127.0.0.1,port=2002;urp;StarOffice.NamingService' -headless
        # 1. prepare data
        context_dict = __post_load_auto(json.loads(item.data))
        context_dict = prepare_context(context_dict, item.type.pk)
        dtlist[item.type.pk - 1]['pe'](context_dict)
	export_function = dtlist[item.type.pk - 1].get('dp', __render_odf)
	return export_function(request, item, context_dict)

def prepare_context(context, type):
    return context
