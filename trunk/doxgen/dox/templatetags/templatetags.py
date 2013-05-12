# -*- coding: utf-8 -*-

from django import template
register = template.Library()

@register.filter
def	strdate(date):
    u'''
    Представляет дату в формате '«01» января 2011 года'.
    '''
    months = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня',
              u'июля', u'августа', u'сентября', u'октября', u'ноября',
              u'декабря')
    return u'«%s» %s %s года' % (date[0:2], months[int(date[3:5]) - 1], date[6:])

@register.filter
def	getorgtype(type):
	return ('Российская', 'Иностранная', 'Иностранная через ОП', 'ИП', 'Нотариус')[int(type) - 1]

@register.filter
def	letterbox(s, l = None):
	'''
	Splits s by l chars
	'''
	retvalue = ''
	if (l):
		s = s.ljust(int(l))
	for c in s:
		retvalue += '<div>'+c+'</div>'
	return retvalue
	#return ('Российская', 'Иностранная', 'Иностранная через ОП', 'ИП', 'Нотариус')[int(type) - 1]

@register.filter
def	sljust(s, lc):
	'''
	rjust string by char
	'''
	#return s
	l, c = lc.split(',')
	if isinstance(s, (int, long)):
		s = unicode(s)
	return s.ljust(int(l), c)
