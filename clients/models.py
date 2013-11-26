# -*- coding: UTF-8 -*-
__author__ = 'sdv'

from django.db import models
from datetime import datetime
#from localflavor.ru.forms import RUPassportNumberField,RUPostalCodeField,RegexField,phone_digits_re,RUCountySelect,RURegionSelect
#from localflavor.ru.ru_regions import RU_COUNTY_CHOICES, RU_REGIONS_CHOICES




class Person(models.Model):
    """
     Базовый класс, описывающий человека (любого) и его свойства:
     - Тип человека по отношения к программе (клиент, сотрудник)
     - Дата создания в базе
     - ФИО
     - Пол
     - Дата рождения
     - Место рождения
     - ИНН (Если есть)
     - ЕНП ОМС
     - СНИЛС
    """
    class Meta:
        abstract = False

    MAN = 'M'
    WOMAN = 'W'
    GENDERS = (
        (MAN, u'Мужской'),
        (WOMAN, u'Женский'),
    )

    EMPLOYEE = 'E'
    CLIENT = 'C'
    PERSON_TYPES = (
    (EMPLOYEE, u'Сотрудник'),
    (CLIENT, u'Клиент'),
)
    personType = models.CharField(max_length=1,choices=PERSON_TYPES,default=CLIENT,verbose_name=u'Тип')
    timestamp = models.DateTimeField(verbose_name=u'Дата создания',default=datetime.now())
    lastName = models.CharField(max_length=50,verbose_name=u'Фамилия')
    firstName = models.CharField(max_length=50,verbose_name=u'Имя')
    middleName = models.CharField(max_length=50,verbose_name=u'Отчество')
    birthDate = models.DateField(verbose_name=u'Дата рождения')
    birthPlace = models.CharField(max_length=100,verbose_name=u'Место рождения')
    gender = models.CharField(max_length=1,choices=GENDERS,default=MAN,verbose_name=u'Пол')
    inn = models.CharField(max_length=12,verbose_name=u'ИНН') # 12 - Физ.лица, 10 - Юр.лица
    enp = models.CharField(max_length=16,verbose_name=u'Единый номер полиса ОМС') # 16 - http://www.rostov-tfoms.ru/o-fonde/96-sistema-oms-na-donu/zasedaniya-rabochikh-grupp/zasedaniya-rabochej-gruppy-po-podgotovke-k-formirovaniyu-i-vedeniyu-erp/364-struktura-edinogo-nomera-polisa-enp-obyazatelnogo-meditsinskogo-strakhovaniya
    snils = models.CharField(max_length=11,verbose_name=u'СНИЛС') # Ex.:123-456-789-12


    def __unicode__(self):
        return self.lastName+' '+self.firstName+' '+self.middleName

    def get_fio(self):
        return self.lastName+' '+self.firstName+' '+self.middleName

    def list_representation_data(self):
        pass

    get_fio.admin_order_field = 'lastName'
    #list_representation_fio.boolean = True
    get_fio.short_description = 'ФИО'



class Document(models.Model):
    D02='02'
    D03='03'
    D04='04'
    D05='05'
    D06='06'
    D07='07'
    D09='09'
    D10='10'
    D11='11'
    D12='12'
    D13='13'
    D14='14'
    D21='21'
    D22='22'
    D23='23'
    D26='26'
    D27='27'
    D91='91'
    DOC_TYPES = (
        (D02, u'Загранпаспорт гражда нина СССР (образца до 1997 года)'),
        (D03, u'Свидетельство о рождении'),
        (D04, u'Удостоверение личности офицера'),
        (D05, u'Справка об освобождении из места лишения свободы'),
        (D06, u'Паспорт Минморфлота'),
        (D07, u'Военный билет солдата (матроса, сержанта, старшины)'),
        (D09, u'Дипломатический паспорт гражданина РФ'),
        (D10, u'Иностранный паспорт (Паспорт иностранного гражданина)'),
        (D11, u'Свидетельство о регистрации ходатайства иммигранта о признании его беженцем'),
        (D12, u'Вид на жительство'),
        (D13, u'Удостоверение беженца в РФ'),
        (D14, u'Временное удостоверение личности гражданина Российской Федерации'),
        (D21, u'Паспорт гражданина Российской Федерации'),
        (D22, u'Загранпаспорт гражданина РФ (образца c 1997 года и позже)'),
        (D23, u'Свидетельство о рождении, выданное уполномоченным органом иностранного государства'),
        (D26, u'Паспорт моряка'),
        (D27, u'Военный билет офицера запаса'),
        (D91, u'Иные документы, выдаваемые органами МВД'),
    )
    docType = models.IntegerField(max_length=2,choices=DOC_TYPES,default=D21)
    series = models.CharField(max_length=20,verbose_name=u'Серия')
    number = models.CharField(max_length=20,verbose_name=u'Номер')
    emitter = models.CharField(max_length=250,verbose_name=u'Кем выдан')
    emitDate = models.DateField(verbose_name=u'Когда выдан')
    emitterCode = models.CharField(max_length=6,verbose_name=u'Код подразделения',blank=True) #123-456
    person = models.ForeignKey(Person,verbose_name=u'Владелец документа')

    def __unicode__(self):
        return self.series+' '+self.number


class Phone(models.Model):
    HOME='H'
    WORK='W'
    MOBILE='M'
    OTHER = 'O'
    PHONE_TYPES = (
        (HOME, u'Домашний'),
        (WORK, u'Рабочий'),
        (MOBILE, u'Мобильный'),
        (OTHER, u'Прочий'),
    )

    phoneType = models.CharField(max_length=1,choices=PHONE_TYPES,default=MOBILE)
    region = models.CharField(max_length=6,verbose_name=u'Регион',blank=True)
    code = models.CharField(max_length=6,verbose_name=u'Код',blank=True)
    number = models.CharField(max_length=7,verbose_name=u'Номер без кодов')
    plainNumber = models.CharField(max_length=25,verbose_name=u'Номер')
    person = models.ForeignKey(Person, verbose_name=u'Владелец')

    def __unicode__(self):
        return '+'+self.region+' ('+self.code+') '+self.number[0:3]+'-'+self.number[3:5]+'-'+self.number[5:7]


class Email(models.Model):
    PRIVATE = 'P'
    WORK = 'W'
    OTHER = 'O'
    EMAIL_TYPES = (
        (PRIVATE, u'Личный'),
        (WORK, u'Рабочий'),
        (OTHER, u'Прочий'),
    )
    emailType = models.CharField(max_length=1,choices=EMAIL_TYPES,default=PRIVATE)
    email = models.EmailField(max_length=200,verbose_name=u'E-mail')
    person = models.ForeignKey(Person, verbose_name=u'Владелец')

    def __unicode__(self):
        return self.email

class Adress(models.Model):
    #TODO: Сделать справочник в полном соответствии с КЛАДР
    LIVE = 'L'
    REGISTER = 'R'
    OTHER = 'O'
    ADRESS_TYPES = (
        (LIVE, u'Адрес фактического проживания'),
        (REGISTER, u'Адрес регистрации'),
        (OTHER, u'Прочий'),
    )
    adressType = models.CharField(max_length=1,verbose_name=u'Тип адреса',choices=ADRESS_TYPES,default=REGISTER,blank=True)
    #region = RURegionSelec
    #country = RUCountySelect
    postalCode = models.CharField(max_length=6,verbose_name=u'Индекс')
    city = models.CharField(max_length=100,verbose_name=u'Город')
    street = models.CharField(max_length=100,verbose_name=u'Улица')
    adress = models.CharField(max_length=50,verbose_name=u'Дом, корпус и квартира')
    person = models.ForeignKey(Person, verbose_name=u'Владелец')


    def __unicode__(self):
        return self.postalCode+', '+self.city+', '+self.street+', '+self.adress


class Positions(models.Model):
    """
    Составлено на основании:
        Приказ № 801н от 25.07.2011
        Об утверждении Номенклатуры должностей медицинского и фармацевтического персонала
        и специалистов с высшим и средним профессиональным образованием учреждений
        здравоохранения (в редакции приказа № 302н от 30.03.2012)
        http://www.spruce.ru/attestation/demands/access/nomenklatura_doljnostei.html

        Примечания:

        1. Наименования должностей заместителей руководителя учреждения здравоохранения
        (главного врача, директора, заведующего, начальника, управляющего) дополняются
        наименованием раздела работы, руководство которой он осуществляет.
        Например, «заместитель главного врача по медицинской части»,
        «заместитель главного врача по работе с сестринским персоналом» и др.

        2. Наименование должности врача формируется с учетом специальности, по которой
        работник имеет соответствующую подготовку и работа по которой вменяется в
        круг его обязанностей. Например, «врач-терапевт».

        3. Наименования должностей руководителей структурных подразделений
        (отделов, отделений, лабораторий, кабинетов, отрядов и др.)
        дополняются наименованием должности врача, соответствующей профилю
        структурного подразделения. Например, «заведующий хирургическим
        отделением - врач-хирург».

        4. В специализированном учреждении здравоохранения или при наличии в учреждении
        здравоохранения соответствующего специализированного подразделения наименование
        должности «врач приемного отделения» дополняется наименованием должности врача
        соответствующей специальности. Например, «врач приемного отделения - врач
        скорой медицинской помощи».

        5. Наименования должностей «акушер», «санитар», «фасовщик»,
        замещаемых лицами женского пола, именуются соответственно: «акушерка»,
        «санитарка», «фасовщица»; а наименование должности «медицинская сестра»,
        замещаемой лицами мужского пола, именуется - «медицинский брат (медбрат)».

    """
    G1 = '0.1'
    G2 = '0.2'
    G3 = '0.3'
    G3_1 = '3.1'
    G3_2 = '3.2'
    G3_3 = '3.3'
    G3_4 = '3.4'
    G3_5 = '3.5'
    G3_6 = '3.6'
    G4 = '0.4'
    G5 = '0.5'
    G6 = '0.6'
    POSITION_LEVELS = (
        (G1, u'I. Руководители учреждений здравоохранения'),
        (G2, u'II. Руководители структурных подразделений (отделов, отделений, лабораторий, кабинетов, отрядов и др.)'),
        (G3_1, u'III Медицинский и фармацевтический персонал: 1) Врачи'),
        (G3_2, u'III Медицинский и фармацевтический персонал: 2) Провизоры'),
        (G3_3, u'III Медицинский и фармацевтический персонал: 3) Средний медицинский персонал'),
        (G3_4, u'III Медицинский и фармацевтический персонал: 4) Средний фармацевтический персонал'),
        (G3_5, u'III Медицинский и фармацевтический персонал: 5) Младший медицинский персонал'),
        (G3_6, u'III Медицинский и фармацевтический персонал: 6) Младший фармацевтический персонал'),
        (G4, u'IV. Специалисты с высшим профессиональным образованием'),
        (G5, u'V. Специалисты со средним профессиональным образованием'),
        (G6, u'ПРОЧИЕ сотрудники, не входящие в классификатор Минздрава'),
    )
    name = models.CharField(max_length=200,verbose_name=u'Наименование должности')
    group = models.CharField(max_length=3,verbose_name=u'Группа',choices=POSITION_LEVELS,default=G6)

    def __unicode__(self):
        return self.name




class Stuff(models.Model):
    position = models.ForeignKey(Positions,verbose_name=u'Должность')
    beginDate = models.DateField(verbose_name=u'Дата приема на работу')
    endDate = models.DateField(verbose_name=u'Дата увольнения',null=True,blank=True)
    payment = models.FloatField(verbose_name=u'Оклад',default=0)

    def __unicode__(self):
        return self.position


class Employee(Person):
    LOW = 'L'
    MIDDLE = 'M'
    HIGH = 'H'
    PC_KNOWLEDGE_LEVELS = (
        (LOW, u'Низкое'),
        (MIDDLE, u'Среднее'),
        (HIGH, u'Высокое'),
    )
    SOCIABILITY_LEVELS = (
        (LOW, u'Низкая общительность'),
        (MIDDLE, u'Средняя общительность'),
        (HIGH, u'Высокая общительность'),
    )
    position = models.ForeignKey(Stuff,verbose_name=u'Занимаемая должность')
    pcKnowledge = models.CharField(max_length=1,verbose_name=u'Уровень владения ПК',choices=PC_KNOWLEDGE_LEVELS,default=MIDDLE)
    sociability = models.CharField(max_length=1,verbose_name=u'Общительность',choices=SOCIABILITY_LEVELS, default=MIDDLE)



class Speciality(models.Model):
    """
    Составлено на основании:
    Приказ № 210н от 23.04.2009
    О номенклатуре специальностей специалистов с высшим и послевузовским медицинским
    и фармацевтическим образованием в сфере здравоохранения Российской Федерации
    http://www.spruce.ru/attestation/demands/access/2009_210.html
    и
    Приказ № 176н от 16.04.2008
    О номенклатуре специалистов со средним медицинским и фармацевтическим образованием
    в сфере здравоохранения Российской Федерации
    (в редакции приказа № 199н от 30.03.2010)
    http://www.spruce.ru/attestation/demands/access/2008_176.html

    """
    vuzSpec = models.CharField(max_length=250,verbose_name=u'Специальность, полученная в ВУЗе')
    mainSpec = models.CharField(max_length=250,verbose_name=u'Основная специальность')
    additionalSpec = models.CharField(max_length=250,verbose_name=u'Специальность, требующая дополнительной подготовки')


class Education(models.Model):
    MIDDLE = 'M'
    HIGH = 'H'
    EDUCATION_TYPES = (
        (MIDDLE, u'Среднее'),
        (HIGH, u'Высшее'),
    )
    educationType = models.CharField(max_length=1,verbose_name=u'Тип образования',choices=EDUCATION_TYPES,default=HIGH)
    university = models.CharField(max_length=100,verbose_name=u'Учебное заведение')
    speciality = models.ForeignKey(Speciality,verbose_name=u'Специальность')
    cvalification = models.CharField(max_length=100,verbose_name=u'Квалификация')
    endDate = models.DateField(verbose_name=u'Дата окончания')
    employee = models.ForeignKey(Employee,verbose_name=u'Сотрудник')



class SkillLevel(models.Model):
    employee = models.ForeignKey(Employee)
    organization = models.CharField(max_length=200,verbose_name=u'Учебное заведение')
    skillDoc = models.CharField(max_length=100,verbose_name=u'Документ подтверждающий обучение')
    dateFrom = models.DateField(verbose_name=u'Дата начала обучения')
    duration = models.CharField(max_length=25,verbose_name=u'Длительность обучения')
    result = models.CharField(max_length=100, verbose_name=u'Присвоенная квалификация (результат)')


class EMC(models.Model):
    num = models.CharField(max_length=8,verbose_name=u'Номер ЭМК')
    registered = models.DateField(verbose_name=u'Дата первичной регистрации')
    def __unicode__(self):
        return u'№: '+self.num+u' от '+self.registered


class ClientCategory(models.Model):
    category = models.CharField(max_length=100,verbose_name=u'Категория')
    def __unicode__(self):
        return self.category

class Disability(models.Model):
    disabilityType = models.CharField(max_length=100,verbose_name=u'Вид инвалидности',blank=True)
    group = models.CharField(max_length=10,verbose_name=u'Группа',blank=True)
    reason = models.CharField(max_length=200,verbose_name=u'Причина',blank=True)
    illness = models.CharField(max_length=100,verbose_name=u'Заболевание',blank=True)
    comment = models.TextField(verbose_name=u'Примечание',blank=True)
    dateFrom = models.DateField(verbose_name=u'Дата получения инвалидности')
    dateTo = models.DateField(verbose_name=u'Дата снятия инвалидности')
    document = models.CharField(max_length=250,verbose_name=u'Документ основания')


class Client(Person):
    MIDDLE = 'M'
    HIGH = 'H'
    EDUCATION_TYPES = (
        (MIDDLE, u'Среднее'),
        (HIGH, u'Высшее'),
    )

    Ip = '1+'
    Im = '1-'
    IIp = '2+'
    IIm = '2-'
    IIIp = '3+'
    IIIm = '3-'
    IVp = '4+'
    IVm = '4-'
    Unknown = 'Unk'
    BLOOD_TYPES = (
        (Ip, u'I+'),
        (Im, u'I-'),
        (IIp, u'II+'),
        (IIm, u'II-'),
        (IIIp, u'III+'),
        (IIIm, u'III-'),
        (IVp, u'IV+'),
        (IVm, u'IV-'),
        (Unknown, u'Неизвестно'),
    )

    emc = models.ForeignKey(EMC,verbose_name=u'Электронная медицинская карта',blank=True,null=True)
    disabilityFlag = models.BooleanField(verbose_name=u'Наличие инвалидности',blank=True)
    disability = models.ForeignKey(Disability,verbose_name=u'Инвалидность',blank=True,null=True)
    source_of_treatment = models.CharField(max_length=100,verbose_name=u'Источник обращения',blank=True)
    educationType = models.CharField(max_length=1,verbose_name=u'Тип образования',choices=EDUCATION_TYPES,default=HIGH)
    category = models.ForeignKey(ClientCategory,verbose_name=u'Категория клиента',blank=True,null=True)
    bloodType = models.CharField(max_length=4,verbose_name=u'Группа крови',choices=BLOOD_TYPES,default=Unknown)



