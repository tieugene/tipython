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
forward_url = 'http://localhost/doxgen/doxgen/'
#forward_url = 'http://dox.eap.su/doxgen/doxgen/'
token = 'fb5168457a495de80c5d7f18205740c2'
#forward_url = 'http://localhost:8000/doxgen/'
#token = '3oquwrX9ayqVvZNkztWtwlvcwpVhJHIP'
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
locality_list = [
	'',
	'Александровская (Курортный район), пос.',
	'Александровская (Пушкинский район), пос.',
	'Белоостров, пос.',
	'Володарская, ст.',
	'Горелово, пос.',
	'Горская, ст.',
	'Комарово, пос.',
	'Лахта, пос.',
	'Левашово, пос.',
	'Лисий Нос, пос.',
	'Металлострой, пос.',
	'Можайская, ст.',
	'Молодежное, пос.',
	'Ольгино, пос.',
	'Парголово, пос.',
	'Песочный, пос.',
	'Петро-Славянка, пос.',
	'Понтонный, пос.',
	'Разлив, ст.',
	'Репино, пос.',
	'Саперный, пос.',
	'Серово, пос.',
	'Смолячково, пос.',
	'Солнечное, пос.',
	'Старо-Паново, дер.',
	'Стрельна, пос.',
	'Тарховка, пос.',
	'Торики, дер.',
	'Тярлево, пос.',
	'Усть-Ижора, пос.',
	'Ушково, пос.',
	'Шушары, пос.',
]
street_type_list = [
	('б-р', 'Бульвар'),
	('въезд', 'Въезд'),
	('дор', 'Дорога'),
	('жт', 'Животноводческая точка'),
	('заезд', 'Заезд'),
	('кв-л', 'Квартал'),
	('км', 'Километр'),
	('кольцо', 'Кольцо'),
	('линия', 'Линия'),
	('наб', 'Набережная'),
	('остров', 'Остров'),
	('парк', 'Парк'),
	('пер', 'Переулок'),
	('переезд', 'Переезд'),
	('пл', 'Площадь'),
	('пл-ка', 'Площадка'),
	('проезд', 'Проезд'),
	('пр-кт', 'Проспект'),
	('просек', 'Просек'),
	('проселок', 'Проселок'),
	('проулок', 'Проулок'),
	('сад', 'Сад'),
	('сквер', 'Сквер'),
	('стр', 'Строение'),
	('тер', 'Территория'),
	('тракт', 'Тракт'),
	('туп', 'Тупик'),
	('ул', 'Улица'),
	('уч-к', 'Участок'),
	('ш', 'Шоссе'),
	('высел', 'Выселки(ок)'),
	('городок', 'Городок'),
	('д', 'Деревня'),
	('ж/д_будка', 'Железнодорожная будка'),
	('ж/д_казарм', 'Железнодорожная казарма'),
	('ж/д_оп', 'ж/д останов. (обгонный) пункт'),
	('ж/д_пост', 'Железнодорожный пост'),
	('ж/д_рзд', 'Железнодорожный разъезд'),
	('ж/д_ст', 'Железнодорожная станция'),
	('казарма', 'Казарма'),
	('м', 'Местечко'),
	('мкр', 'Микрорайон'),
	('нп', 'Населенный пункт'),
	('платф', 'Платформа'),
	('п', 'Поселок'),
	('п/о', 'Почтовое отделение'),
	('п/р', 'Планировочный район'),
	('п/ст', 'Поселок и(при) станция(и)'),
	('полустанок', 'Полустанок'),
	('починок', 'Починок'),
	('рзд', 'Разъезд'),
	('с', 'Село'),
	('сл', 'Слобода'),
	('ст', 'Станция'),
	('х', 'Хутор'),
	('ж/д_платф', 'Железнодорожная платформа'),
	('спуск', 'Спуск'),
	('канал', 'Канал'),
	('гск', 'Гаражно-строительный кооперат'),
	('снт', 'Садовое неком-е товарищество'),
	('лпх', 'Леспромхоз'),
	('проток', 'Проток'),
	('коса', 'Коса'),
	('вал', 'Вал'),
	('ферма', 'Ферма'),
	('мост', 'Мост'),
	('ряды', 'Ряды'),
	('а/я', 'Абонентский ящик'),
	('берег', 'Берег'),
	('просека', 'Просека'),
	('протока', 'Протока'),
	('бугор', 'Бугор'),
	('зона', 'Зона'),
	('днп', 'Дачное неком-е партнерство'),
	('н/п', 'Некоммерческое партнерство'),
	('ф/х', 'Фермерское хозяйство'),
]
building_type_list = [
	('', '---'),
	('корп', 'корпус'),
	('стр', 'строение'),
	('лит', 'литер'),
]
app_type_list = [
	('', '---'),
	('кв', 'квартира'),
	('пом', 'помещение'),
	('оф', 'офис'),
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
	web.form.Textbox('lastname',		chk_empty, description='Фамилия', size='34', maxlength='34'),
	web.form.Textbox('firstname',		chk_empty, description='Имя', size='34', maxlength='34'),
	web.form.Textbox('midname',		description='Отчество', size='34', maxlength='34'),
	web.form.Dropdown('sex',		description='Пол', args=sex_list, value='1'),
	web.form.Textbox('birthdate',		chk_empty, chk_date, ChkDate(), description='Дата рождения'),
	web.form.Textbox('birthplace',		chk_empty, description='Место рождения', maxlength='80'),
	web.form.Textbox('inn',			ChkInn(), description='ИНН', size='12'),
	web.form.Textbox('addr_zip',		chk_empty, chk_6, description='Индекс', size='6', minlength='6', maxlength='6'),
	web.form.Dropdown('addr_locality',	description='Населенный пункт', args=locality_list),
	web.form.Dropdown('addr_street_type',	description='Улица.Тип', args=street_type_list, value='ул'),
	web.form.Textbox('addr_street_name',	chk_empty, description='Улица.Наименование', maxlength='68'),
	web.form.Textbox('addr_house_name',	chk_empty, description='Дом', maxlength='8'),
	web.form.Dropdown('addr_building_type',	description='Корпус.Тип', args=building_type_list),
	web.form.Textbox('addr_building_name',	description='Корпус.Номер', maxlength='8'),
	web.form.Dropdown('addr_app_type',	description='Квартира.Тип', args=app_type_list),
	web.form.Textbox('addr_app_name',	description='Квартира.Номер', maxlength='8'),
	web.form.Textbox('doc_series',		chk_empty, chk_4, description='Серия', size='4', minlength='4', maxlength='4'),
	web.form.Textbox('doc_no',		chk_empty, chk_6, description='Номер', size='6', minlength='6', maxlength='6'),
	web.form.Textbox('doc_date',		chk_empty, chk_date, ChkDate(), description='Дата', size='10'),
	web.form.Textbox('doc_who',		chk_empty, description='Кем выдан', maxlength='114'),
	web.form.Textbox('doc_kp',		chk_empty, chk_6, description='Код подразделения', size='6', minlength='6', maxlength='6'),
	web.form.Textbox('phone_code',		description='Код', size='5', maxlength='5'),
	web.form.Textbox('phone_no',		description='Телефон', size='7', maxlength='7'),
	web.form.Textbox('email',		description='E-mail'),
	web.form.Dropdown('todo',		description='Что делать с документами', args=todo_list, value='1'),
	web.form.Dropdown('tax',		description='Налогообложение', args=tax_list),
	#web.form.Checkbox('selected',		description='ОКВЭДы'),
	validators = [web.form.Validator('Добавьте хотя бы один ОКВЭД', lambda i: len(web.input(selected=[]).selected))]
)

def	prepare_21001(f, addr, selected):
	locality = f.addr_locality.get_value()
	if locality:
		locality = locality.rsplit(' ', 1)
		ltype = locality[0].rstrip(',')
		lname = locality[1].rstrip('.')
	else:
		ltype = ''
		lname = ''
	retvalue = {
		'csrfmiddlewaretoken':	token,
		'_action':		'print',
		'lastname':		f.lastname.get_value(),
		'firstname':		f.firstname.get_value(),
		'midname':		f.midname.get_value(),
		'sex':			f.sex.get_value(),
		'birthdate':		f.birthdate.get_value(),
		'birthplace':		f.birthplace.get_value(),
		'citizenship':		'1',
		'addr_zip':		f.addr_zip.get_value(),
		'addr_srf':		'78',
		'addr_locality_type':	ltype,
		'addr_locality_name':	lname,
		'addr_street_type':	f.addr_street_type.get_value(),
		'addr_street_name':	f.addr_street_name.get_value(),
		'addr_house_type':	'дом',
		'addr_house_name':	f.addr_house_name.get_value(),
		'addr_building_type':	f.addr_building_type.get_value(),
		'addr_building_name':	f.addr_building_name.get_value(),
		'addr_app_type':	f.addr_app_type.get_value(),
		'addr_app_name':	f.addr_app_name.get_value(),
		'doc_type':		21,
		'doc_series_no':	'%s %s %s' % (f.doc_series.get_value()[:2], f.doc_series.get_value()[2:], f.doc_no.get_value()),
		'doc_date':		f.doc_date.get_value(),
		'doc_whom':		f.doc_who.get_value(),
		'doc_kp':		f.doc_kp.get_value(),
		'inn':			f.inn.get_value(),
		'phone':		'+7(%s)%s' % (f.phone_code.get_value(), f.phone_no.get_value()) if f.phone_no.get_value() else '',
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
			addr = f.addr_zip.get_value() + ', г. Санкт-Петербург, '
			if (f.addr_locality.get_value()):
				addr = addr + f.addr_locality.get_value() + ', '
			addr = addr + f.addr_street_type.get_value() + '. ' + f.addr_street_name.get_value() + ', д. ' + f.addr_house_name.get_value()
			if (f.addr_building_type.get_value()):
				addr = addr + ', ' + f.addr_building_type.get_value() + '. ' + f.addr_building_name.get_value()
			if (f.addr_app_type.get_value()):
				addr = addr + ', ' + f.addr_app_type.get_value() + '. ' + f.addr_app_name.get_value()
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
				#print r.status_code, r.raw.read()
				return r.text
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
