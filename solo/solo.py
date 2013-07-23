#!/bin/env python
# -*- coding: utf-8 -*-
'''
example: http://ip-nalog.ru/forma-p21001-1.html
TODO:
	* set okveds on error
	* addr_*_type - dropdowns:
	-- корпус, строение, лит
	-- квартира, помещение, офис
	* addr_locality - dropdown (http://www.mk-kadar.ru/service/ipdocs.htm)
'''

# 3rd parties
import web, pyPdf, requests
# system
import sys, os, tempfile, pprint, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

debug = True
cache = False
#forward_url = 'http://localhost/doxgen/doxgen/'
forward_url = 'http://dox.eap.su/doxgen/doxgen/'
token = '59aeb29436ed7c3328ff58dd46ba5b0a'
try:
        from local_settings import *
except ImportError:
        pass
db = web.database(dbn='sqlite', db='solo.db')
render = web.template.render('', cache=cache)

forms = {
	'21001':	'BD265452F0434603AA201EF4077D68D9',	# z0008:	Заявление о регистрации ИП (от 04.07.2013)
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
todo_list = [
	('1', 'Выдать заявителю'),
	('2', 'Выдать заявителю или лицу, действующему на основании доверенности'),
	('3', 'Отправить по почте'),
]
location_list = [
	('1',  'Александровская (Курортный район), пос.'),
	('2',  'Александровская (Пушкинский район), пос.'),
	('3',  'Белоостров, пос.'),
	('4',  'Володарская, ст.'),
	('5',  'Горелово, пос.'),
	('6',  'Горская, ст.'),
	('7',  'Комарово, пос.'),
	('8',  'Лахта, пос.'),
	('9',  'Левашово, пос.'),
	('10', 'Лисий Нос, пос.'),
	('11', 'Металлострой, пос.'),
	('12', 'Можайская, ст.'),
	('13', 'Молодежное, пос.'),
	('14', 'Ольгино, пос.'),
	('15', 'Парголово, пос.'),
	('16', 'Песочный, пос.'),
	('17', 'Петро-Славянка, пос.'),
	('18', 'Понтонный, пос.'),
	('19', 'Разлив, ст.'),
	('20', 'Репино, пос.'),
	('21', 'Саперный, пос.'),
	('22', 'Серово, пос.'),
	('23', 'Смолячково, пос.'),
	('24', 'Солнечное, пос.'),
	('25', 'Старо-Паново, дер.'),
	('26', 'Стрельна, пос.'),
	('27', 'Тарховка, пос.'),
	('28', 'Торики, дер.'),
	('29', 'Тярлево, пос.'),
	('30', 'Усть-Ижора, пос.'),
	('31', 'Ушково, пос.'),
	('32', 'Шушары, пос.'),
]
#	-- корпус, строение, лит
#	-- квартира, помещение, офис
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
	web.form.Textbox('lastname',		chk_empty, description='Фамилия', size='34', maxlength='34'),
	web.form.Textbox('firstname',		chk_empty, description='Имя', size='34', maxlength='34'),
	web.form.Textbox('midname',		description='Отчество', size='34', maxlength='34'),
	web.form.Dropdown('sex',		description='Пол', args=sex_list, value='1'),
	web.form.Textbox('birthdate',		chk_empty, chk_date, ChkDate(), description='Дата рождения'),
	web.form.Textbox('birthplace',		chk_empty, description='Место рождения', maxlength='80'),
	web.form.Textbox('inn',			ChkInn(), description='ИНН', size='12'),
	web.form.Textbox('addr_zip',		chk_empty, chk_6, description='Индекс', size='6'),	# minlength, maxlength
	web.form.Textbox('addr_locality_type',	description='Населенный пункт.Тип', maxlength='10'),
	web.form.Textbox('addr_locality_name',	description='Населенный пункт.Наименование', maxlength='68'),
	web.form.Textbox('addr_street_type',	chk_empty, description='Улица.Тип', maxlength='10'),
	web.form.Textbox('addr_street_name',	chk_empty, description='Улица.Наименование', maxlength='68'),
	web.form.Textbox('addr_house_type',	chk_empty, description='Дом.Тип', maxlength='10'),
	web.form.Textbox('addr_house_name',	chk_empty, description='Дом.Номер', maxlength='8'),
	web.form.Textbox('addr_building_type',	description='Корпус (строение).Тип', maxlength='10'),
	web.form.Textbox('addr_building_name',	description='Корпус (строение).Номер', maxlength='8'),
	web.form.Textbox('addr_app_type',	description='Квартира (офис, помещение).Тип', maxlength='8'),
	web.form.Textbox('addr_app_name',	description='Квартира (офис, помещение).Номер', maxlength='8'),
	web.form.Textbox('doc_series',		chk_empty, chk_4, description='Серия', size='4'),
	web.form.Textbox('doc_no',		chk_empty, chk_6, description='Номер', size='6'),
	web.form.Textbox('doc_date',		chk_empty, chk_date, ChkDate(), description='Дата', size='10'),
	web.form.Textbox('doc_who',		chk_empty, description='Кем выдан', maxlength='114'),
	web.form.Textbox('doc_kp',		chk_empty, chk_6, description='Код подразделения', size='6'),
	web.form.Textbox('phone_code',		description='Код', size='5'),
	web.form.Textbox('phone_no',		description='Телефон', size='7'),
	web.form.Textbox('email',		description='E-mail'),
	web.form.Dropdown('todo',		description='Что делать', args=todo_list, value='1'),
	web.form.Dropdown('tax',		description='Налогообложение', args=tax_list),
	#web.form.Checkbox('selected',		description='ОКВЭДы'),
	validators = [web.form.Validator('Добавьте хотя бы один ОКВЭД', lambda i: len(web.input(selected=[]).selected))]
)

def	prepare_21001(f, addr, selected):
	retvalue = {
		'csrfmiddlewaretoken':	token,
		'_action':		'print',
		'lastname':		f.lastname.get_value(),
		'firstname':		f.firstname.get_value(),
		'midname':		f.midname.get_value(),
		'sex':			('мужской', 'женский')[int(f.sex.get_value())-1],
		'birthdate':		f.birthdate.get_value(),
		'birthplace':		f.birthplace.get_value(),
		'citizenship':		'1',
		'addr_zip':		f.addr_zip.get_value(),
		'addr_srf':		'78',
		'addr_city_type':	'г',
		'addr_city_name':	'Санкт-Петербург',
		'addr_locality_type':	f.addr_locality_type.get_value(),
		'addr_locality_name':	f.addr_locality_name.get_value(),
		'addr_street_type':	f.addr_street_type.get_value(),
		'addr_street_name':	f.addr_street_name.get_value(),
		'addr_house_type':	f.addr_house_type.get_value(),
		'addr_house_name':	f.addr_house_name.get_value(),
		'addr_building_type':	f.addr_building_type.get_value(),
		'addr_building_name':	f.addr_building_name.get_value(),
		'addr_app_type':	f.addr_app_type.get_value(),
		'addr_app_name':	f.addr_app_name.get_value(),
		'phone':		'+7 %s %s' % (f.phone_code.get_value(), f.phone_no.get_value()),
		'doc_type':		21,
		'doc_series_no':	f.doc_series.get_value() + ' ' + f.doc_no.get_value(),
		'doc_date':		f.doc_date.get_value(),
		'doc_whom':		f.doc_who.get_value(),
		'doc_kp':		f.doc_kp.get_value(),
		'inn':			f.inn.get_value(),
		'email':		f.email.get_value(),
		'todo':			f.todo.get_value(),
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
			# FIXME:
			addr = \
				f.addr_zip.get_value() + \
				', г. Санкт-Петербург, ' + \
				f.addr_street_type.get_value() + '. ' + f.addr_street_name.get_value() + ', ' + \
				f.addr_house_type.get_value() + ' ' + f.addr_house_name.get_value()
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
