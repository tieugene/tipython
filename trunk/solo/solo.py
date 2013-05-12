#!/bin/env python
# -*- coding: utf-8 -*-
'''
TODO:
	* set okveds on error
'''

# 3rd parties
import web, pyPdf, requests
# system
import sys, os, tempfile, pprint, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

debug = True
cache = False
try:
        from local_settings import *
except ImportError:
        pass
db = web.database(dbn='sqlite', db='solo.db')
render = web.template.render('', cache=cache)

forward_url = 'http://localhost/doxgen/doxgen/'
token = '59aeb29436ed7c3328ff58dd46ba5b0a'
forms = {
	'21001':	'C9B0FA3ACED04F5E88131626A3881BBF',	# z0002:	Заявление о регистрации ИП
	'pd4':		'98A391C4F45C4A2AA21A69E6C16592EC',	# z0003:	Квитацния в этот ваш Сбер
	'usn':		'D6A364487A1E4E7F853BCC4CA47B4E8D',	# z0007:	Зая об УСН
}
sex_list = [
	('1', 'мужской'),
	('2', 'женский'),
]
tax_list = [
	('1', 'ЕНВД'),
	('2', 'ОСН (общая, НДС)'),
	('3', 'УСН (доходы)'),
	('4', 'УСН (доходы - расходы)'),
]

# validators
chk_empty = web.form.Validator('Обязательное поле', bool)
chk_date = web.form.regexp('^(3[01]|[12][0-9]|0[1-9])\.(1[0-2]|0[1-9])\.[0-9]{4}$', 'Не похоже на дату (ДД.ММ.ГГГГ)')
chk_4 = web.form.regexp('^[0-9]{4}$', 'Должно быть 4 цифры')
chk_6 = web.form.regexp('^[0-9]{6}$', 'Должно быть 6 цифр')

class	ChkDate(web.form.Validator):
	def	__init__(self):
		self.msg = 'Неверная дата'
	def	valid(self, value):
		try:
			datetime.datetime.strptime(value, '%d.%m.%Y')
		except:
			return False
		else:
			return True

class	ChkInn(web.form.Validator):
	def	__chk_cs(self, s, k):
		sum = 0
		l = len(k)
		for i in xrange(l):
			sum += int(s[i]) * k[i]
		#print ((sum%11)%10)%11
		return ((sum%11)%10)%11 == int(s[l])
	def	__init__(self):
		self.msg = None
	def	valid(self, value):
		if (not value):
			return True
		if (not value.isdigit()):
			self.msg = 'Должны быть только цифры'
			return False
		if (len(value) != 12):
			self.msg = 'Должно быть именно 12 цифр'
			return False
		if (self.__chk_cs(value, (7, 2, 4, 10, 3, 5, 9, 4, 9, 8)) and self.__chk_cs(value, (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8))):
			return True
		else:
			self.msg = 'Контрольные суммы цифры неверны'
			return False

ip_form = web.form.Form(
	web.form.Textbox('lastname',		chk_empty, description='Фамилия'),
	web.form.Textbox('firstname',		chk_empty, description='Имя'),
	web.form.Textbox('midname',		description='Отчество'),
	web.form.Dropdown('sex',		description='Пол', args=sex_list, value='1'),
	web.form.Textbox('birthdate',		chk_empty, chk_date, ChkDate(), description='Дата рождения'),
	web.form.Textbox('birthplace',		chk_empty, description='Место рождения'),
	web.form.Textbox('inn',			ChkInn(), description='ИНН', size='12'),
	web.form.Textbox('addr_zip',		chk_empty, chk_6, description='Индекс', size='6'),	# minlength, maxlength
	web.form.Textbox('addr_locality',	description='Населенный пункт'),
	web.form.Textbox('addr_street',		chk_empty, description='Улица'),
	web.form.Textbox('addr_house',		chk_empty, description='Дом'),
	web.form.Textbox('addr_building',	description='Корпус (строение)'),
	web.form.Textbox('addr_app',		description='Квартира (офис, помещение)'),
	web.form.Textbox('phone_code',		description='Код', size='5'),
	web.form.Textbox('phone_no',		description='Телефон', size='7'),
	web.form.Textbox('phone_fax',		description='Факс', size='7'),
	web.form.Textbox('doc_series',		chk_empty, chk_4, description='Серия', size='4'),
	web.form.Textbox('doc_no',		chk_empty, chk_6, description='Номер', size='6'),
	web.form.Textbox('doc_date',		chk_empty, chk_date, ChkDate(), description='Дата'),
	web.form.Textbox('doc_who',		chk_empty, description='Кем выдан'),
	web.form.Textbox('doc_kp',		chk_empty, chk_6, description='Код подразделения', size='6'),
	web.form.Dropdown('tax',		description='Налогообложение', args=tax_list),
	#web.form.Checkbox('selected',		description='ОКВЭДы'),
	validators = [web.form.Validator('Добавьте хотя бы один ОКВЭД', lambda i: len(web.input(selected=[]).selected))]
)

def	prepare_21001(f, addr, selected):
	retvalue = {
		'csrfmiddlewaretoken':	token,
		'_action':		'print',
		'spro_name':		'Межрайонную Инспекцию ФНС России № 15 по Санкт-Петербургу',
		'spro_id':		'78086',
		'lastname':		f.lastname.get_value(),
		'firstname':		f.firstname.get_value(),
		'midname':		f.midname.get_value(),
		'sex':			('мужской', 'женский')[int(f.sex.get_value())-1],
		'birthdate':		f.birthdate.get_value(),
		'birthplace':		f.birthplace.get_value(),
		'citizenship':		'1',
		'addr_zip':		f.addr_zip.get_value(),
		'addr_srf':		'78',
		'addr_locality':	f.addr_locality.get_value(),
		'addr_street':		f.addr_street.get_value(),
		'addr_house':		f.addr_house.get_value(),
		'addr_building':	f.addr_building.get_value(),
		'addr_app':		f.addr_app.get_value(),
		'phone_code':		f.phone_code.get_value(),
		'phone_no':		f.phone_no.get_value(),
		'phone_fax':		f.phone_fax.get_value(),
		'doc_type':		'паспорт гражданина РФ',
		'doc_series':		f.doc_series.get_value(),
		'doc_no':		f.doc_no.get_value(),
		'doc_date':		f.doc_date.get_value(),
		'doc_whom':		f.doc_who.get_value(),
		'doc_kp':		f.doc_kp.get_value(),
		'inn':			f.inn.get_value(),
		'okved-TOTAL_FORMS':	len(selected),
		'okved-INITIAL_FORMS':	0,
		'okved-MAX_NUM_FORMS':	'',
	}
	for i, v in enumerate(selected):
		retvalue['okved-%d-code' % i] = v.replace('_', '.').lstrip('a')
	return retvalue

def	prepare_pd4(f, addr, selected):
	return {
		'csrfmiddlewaretoken':	token,
		'_action':		'print',
		'recipient':		'МИ ФНС РФ №11 по Санкт-Петербургу',
		'recishort':		'УФК МФ РФ по СПб',
		'inn':			'7842000011',
		'kpp':			'784201001',
		'okato':		'40298564000',
		'account':		'40101810200000010001',
		'bank':			'ГРКЦ ГУ Банка России по Санкт-Петербургу',
		'bik':			'044030001',
		#'ks':			'ks',
		'kbk':			'18210807010011000110',
		'details':		'за государственную регистрацию физ.лиц, ИП',
		'payer_fio':		f.lastname.get_value() + ' ' + f.firstname.get_value() + ' ' + f.midname.get_value(),
		'payer_address':	addr,
		'payer_inn':		f.inn.get_value(),
		'total':		'800.00',
		'date':			datetime.datetime.today().strftime('%d.%m.%Y'),
	}

def	prepare_usn(f, addr, selected):
	return {
		'csrfmiddlewaretoken':	token,
		'_action':		'print',
		'inn':			f.inn.get_value(),	# ???
		'kno':			'7801',
		'app_sign':		'1',			# ???
		'org_name':		f.lastname.get_value() + ' ' + f.firstname.get_value() + ' ' + f.midname.get_value(),
		'chg_type':		'2',
		'tax_obj':		str(int(f.tax.get_value()) - 2),
		'petition_year':	str(datetime.datetime.today().year),	# ???
		'app_type':		'1',
		'delegate_date':	datetime.datetime.today().strftime('%d.%m.%Y'),
	}

def	deltmp(tmplist):
	for i in tmplist:
		os.remove(i.name)

def	get_okveds():
	return db.select('okved', order='id')

def	get_okved(id):
	return db.query("SELECT name FROM okved WHERE okved.id = '%s'" % id)[0].name

class	index:
	def	GET(self):
		return render.form(ip_form(), get_okveds(), [])
	def	POST(self):
		f = ip_form()
		selected = web.input(selected=[]).selected	# ['a_01_1', ...]
		if not f.validates():
			selected_list = []
			#for i in selected:
			#	id = i.replace('_', '.').lstrip('a')
			#	selected_list.append((i, id, get_okved(id)))
			return render.form(f, get_okveds(), selected_list)
		else:
			addr = f.addr_zip.get_value() + ', Санкт-Петербург, ' + f.addr_street.get_value() + ', ' + f.addr_house.get_value()
			output = pyPdf.PdfFileWriter()
			error = False
			tmpfile = list()
			tocall = [('21001', prepare_21001), ('pd4', prepare_pd4)]
			if (int(f.tax.get_value()) > 2):
				tocall.append(('usn', prepare_usn,),)
			for key, func in tocall:
				url = forward_url + forms[key] + '/a/'
				r = requests.post(url, data=func(f, addr, selected), cookies=dict(csrftoken=token))
				if (r.status_code == 200):	# r - Responce object
					if (r.headers['content-type'] == 'application/pdf'):
						tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
						tmp.write(r.content)
						input = pyPdf.PdfFileReader(tmp)
						for page in input.pages:
							output.addPage(page)
						tmpfile.append(tmp)
					else:	# e.g. 'text/html; charset=utf-8'
						error = True
				else:
					error = True
					deltmp(tmpfile)
					break
			if error:
				deltmp(tmpfile)
				return r.raw.read()
			else:
				web.header('Content-Type', 'application/pdf')
				web.header('Content-Transfer-Encoding', 'binary')
				web.header('Content-Disposition', 'attachment; filename=\"print.pdf\";')
				outputStream = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
				output.write(outputStream)
				outputStream.close()
				retvalue = file(outputStream.name, 'rb').read()
				os.remove(outputStream.name)
				deltmp(tmpfile)
				return retvalue
# 1. standalone
if __name__ == '__main__':
	app = web.application(('/', 'index'), globals())
	app.internalerror = web.debugerror
	app.run()
# 2. apache mod_wsgi
os.chdir(os.path.dirname(__file__))
application = web.application(('/', 'index'), globals()).wsgifunc()
