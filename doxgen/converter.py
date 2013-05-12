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
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader

# 2. system
import tempfile, datetime, sys, os, subprocess, time

# 3. 3rd party
import wkhtmltopdf	#, rml2pdf
import wkhtmltox

reload(sys)
sys.setdefaultencoding('utf-8')

def	html2html(request, context_dict, template):
	return render_to_response(template, context_instance=RequestContext(request, context_dict))

def	html2pdf(request, context_dict, template):
	'''
	Render [x]html to pdf
	:param request - request
	:param context_dict - dictionary of data
	:param template - path of tpl
	'''
	# 1. prepare
	tmp = tempfile.NamedTemporaryFile(suffix='.xhtml', delete=True)		# delete=False to debug
	tmp.write(render(request, template, context_instance=Context(context_dict), content_type='text/xml').content)
	tmp.flush()
	outfile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=True)	# delete=False to debug
	# 2. render - new style
	#pdf = wkhtmltox.Pdf()
	#pdf.set_global_setting('out', outfile.name)
	#pdf.add_page({'page': 'file://%s' % os.path.abspath(tmp.name)})
	#pdf.convert()
	# 2. render - old style
	wkh = wkhtmltopdf.WKhtmlToPdf(tmp.name, outfile.name, dpi=300)	# header_left='"Powered by http://dox.mk-kadar.ru"', header_font_size=6)
	wkh.render()
	# 3. response
	response = HttpResponse(content=outfile.read(), mimetype='application/pdf', content_type = 'application/pdf')
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = (u'attachment; filename=\"print.pdf\";')
	# 4. cleanup
	#if (os.path.exists(outfile.name)):
	#	os.remove(outfile.name)	# hack
	return response

def	rml2pdf(request, context_dict, template):
	'''
	Create pdf from rml-template and return file to user
	'''
	response = HttpResponse(mimetype='application/pdf', content_type = 'application/pdf')
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = (u'attachment; filename=\"print.pdf\";')
	tpl = loader.get_template(template)
	tc = {'STATIC_ROOT' : settings.STATIC_ROOT}
	tc.update(context_dict)
	response.write(rml2pdf.parseString(tpl.render(Context(tc)).encode('utf-8')))
	#response.write(tpl.render(Context(tc)).encode('utf-8'))
	return response

def	xfdf2pdf(request, context_dict, template):
	'''
	@param template: xfdf-file
	@param pdfname: pdf form
	1. render xfdf to stdout
	2. merge pdf and stdin to stdout (pdftk <template.pdf> fill_form <data.xfdf>|- output <out.pdf>|-)
	'''
	pdftpl = os.path.join(settings.PROJECT_DIR, 'templates', template.rsplit('.', 1)[0] + '.pdf')
	out, err = subprocess.Popen(['xfdftool', '-f', pdftpl], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(str(loader.get_template(template).render(Context(context_dict))))
	if (err):
		#response = HttpResponse('We had some errors:<pre>%s</pre>' % escape(err) + pdftpl)
		response = HttpResponse('We had some errors:<pre>%s</pre>' % err + pdftpl)
	else:
		response = HttpResponse(content_type = 'application/pdf')
		response['Content-Transfer-Encoding'] = 'binary'
		response['Content-Disposition'] = (u'attachment; filename=\"print.pdf\";')
		response.write(out)
	return response

def	odf2pdf(request, context_dict, template):
        # 2. render: need request, context_dict
	doc = request.POST['doc']	# 0..E (string)
	tplname = 'doc_0004_%s' % doc	# FIXME:
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

x2pdf = {
	'htm':		html2pdf,
	'html':		html2pdf,
	'xhtm':		html2pdf,
	'xhtml':	html2pdf,
	'rml':		rml2pdf,
	'xfdf':		xfdf2pdf,
	'fodt':		odf2pdf,
	'fods':		odf2pdf,
	'fodp':		odf2pdf,
}
