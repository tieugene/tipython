# -*- coding: utf-8 -*-
'''
Converters module
Params:
	* request: request
	* context_dict: data
	* template:str - path to template (.../*.html/fodf/rml)
Returns: HttpResponse object
	
Input:
	* [x]htm[l] => [html/]pdf
	* rml => pdf
	* fodf => pdf/*
Try:
	* lyx => pdf (too long; lyx -e)
	* svg (webkit, inkscape (pyqt))
	* scribus (pyqt) - don't know
	* html5 (webkit)
	* pdf forms (pdftk)
'''

# 1. django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader

# 2. system
import tempfile, datetime

# 3. 3rd party
import wkhtmltopdf

def	html2html(request, context_dict, template):
	return render_to_response(template, context_instance=RequestContext(request, context_dict))

def	html2pdf(request, context_dict, template):
	'''
	Render [x]html to pdf
	:param request - request
	:param context_dict - dictionary of data
	:param template - path of tpl
	'''
	# 1. render: need request, context_dict
	tmp = tempfile.NamedTemporaryFile(suffix='.xhtml', delete=True)		# delete=False to debug
	tmp.write(render(request, template, context_instance=Context(context_dict), content_type='text/xml').content)
	tmp.flush()
	outfile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=True)	# delete=False to debug
	wkh = wkhtmltopdf.WKhtmlToPdf(tmp.name, outfile.name, dpi=300, header_left='"Powered by http://dox.mk-kadar.ru"', header_font_size=6)
	wkh.render()
	# 2. response
	response = HttpResponse(content=outfile.read(), mimetype='application/pdf', content_type = 'application/pdf')
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = (u'attachment; filename=\"print.pdf\";')
	#if (os.path.exists(outfile.name)):
	#	os.remove(outfile.name)	# hack
	return response

def	rml2pdf(request, context_dict, template):
	'''
	Create pdf from rml-template and return file to user
	'''
	filename = template+'.pdf'
	response = HttpResponse(mimetype='application/pdf', content_type = 'application/pdf')
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = (u'attachment; filename=\"print.pdf\";')
	tpl = loader.get_template(template)
	tc = {'filename': filename, 'STATIC_ROOT' : settings.STATIC_ROOT}
	tc.update(context)
	response.write(trml2pdf.parseString(tpl.render(Context(tc)).encode('utf-8')))
	#response.write(tpl.render(Context(tc)).encode('utf-8'))
	return response

def	fdf2pdf(request, context_dict, template, pdfname):
	'''
	@param template: fdf
	@param pdfname: pdf form
	1. render fdf to stdout
	2. merge pdf and stdin to stdout (or tmp?)
	'''
	# 1. render xfdf
	xfdf = loader.get_template(template).render(Context(context_dict))
	# 2. merge: pdftk <template.pdf> fill_form <data.xfdf>|- output <out.pdf>|-
	pdftpl = os.path.join(settings.PROJECT_DIR, 'templates', pdfname)
	pdftpl = '/home/artem/django_projects/doxgen/templates/docentity_print_01_02.pdf'
	#print pdftpl

	out, err = subprocess.Popen(['pdftk', pdftpl, 'fill_form', '-', 'output', '-'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(xfdf)
	if (err):
		response = HttpResponse('We had some errors:<pre>%s</pre>' % escape(err) + pdftpl)
	else:
		response = HttpResponse(content_type = 'application/pdf')
		response['Content-Transfer-Encoding'] = 'binary'
		response['Content-Disposition'] = (u'attachment; filename=\"F11001.pdf\";')
		response.write(out)
		#response.write(open(os.path.join('templates', pdfname)).read())
	return response

def	odf2pdf(request, context_dict, template):
        # 2. render: need request, context_dict
	doc = request.POST['doc']	# 0..E (string)
	tplname = 'doc_0004_%s' % doc
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
