# -*- coding: utf-8 -*-

from django import forms

from models import *
###(1
from gw.models import *
###1)

class    SroForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = Sro
        exclude = ('own')
        
class    SroOwnForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = SroOwn
#        fields = ('name', 'shortname', 'fullname', 'okopf', 'egruldate', 'inn', 'kpp', 'foreign', 'ogrn', 'okato', 'laddress', 'raddress', 'comments')
        exclude = ('sro', 'path', 'sshhost', 'ftp', 'bosstitle', 'tplprefix', 'boss')

class    OrgListForm(forms.Form):
    okato        = forms.ModelChoiceField(queryset=Okato.objects.all(), required=False)
    insurer        = forms.ModelChoiceField(queryset=Insurer.objects.all(), required=False)
    okato.widget.attrs["onchange"]="this.form.submit()"
    insurer.widget.attrs["onchange"]="this.form.submit()"


class    AllOrgsForm(forms.Form):
    org        = forms.ModelChoiceField(queryset=OrgSro.objects.all())

    def    setdata(self,sro):
        self.fields['org'].queryset = OrgSro.objects.filter(sro=sro)

class    OrgAddExistsForm(forms.Form):
    org        = forms.ModelChoiceField(queryset=Org.objects.all())
    def    __init__(self, sro, *args, **kwargs):
        super(OrgAddExistsForm, self).__init__(*args, **kwargs)
        self.fields['org'].queryset = Org.objects.exclude(id__in=sro.orgsro_set.values_list('org', flat=True).exclude(status=3))

class    OrgAddForm(forms.ModelForm):
    fullname    = forms.CharField(label='Полное наименование', widget=forms.Textarea)
    egruldate    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата регистрации в ЕГРЮЛ', required=False)
#    laddress    = forms.CharField(label='Юридический адрес', widget=forms.Textarea)
#    raddress    = forms.CharField(label='Фактический адрес', widget=forms.Textarea, required=False)
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = Org
        fields = ('name', 'shortname', 'fullname', 'okopf', 'egruldate', 'inn', 'kpp', 'foreign', 'ogrn', 'okato', 'comments')
        #exclude = ('okveds', 'stuffs', 'user', 'brandname')

class    OrgEditForm(forms.ModelForm):
    fullname    = forms.CharField(label='Полное наименование', widget=forms.Textarea)
    egruldate   = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата регистрации в ЕГРЮЛ', required=False)
#    laddress    = forms.CharField(label='Юридический адрес', widget=forms.Textarea)
#    raddress    = forms.CharField(label='Фактический адрес', widget=forms.Textarea, required=False)
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = Org
        fields = ('name', 'shortname', 'fullname', 'okopf', 'egruldate', 'inn', 'kpp', 'foreign', 'ogrn', 'okato', 'comments')
        #exclude = ('okveds', 'stuffs', 'user', 'brandname',)

class    OrgSroForm(forms.ModelForm):
    #regdate        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата членства в НП', required=False)
    paydate        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата оплаты взноса в КФ', required=False)
    paydatevv    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата оплаты вступительного взноса', required=False)
    class    Meta:
        model = OrgSro
        exclude = ('org', 'sro', 'events', 'user', 'agent', 'currperm', 'regno','regdate','speccase','speccomments','status','protocol','reason','excludedate','inprotocol')

class    OrgLicenseForm(forms.ModelForm):
    no        = forms.CharField(label='Номер', widget=forms.Textarea)
    datefrom    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Действует с')
    datedue        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Действительна до')
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = OrgLicense
        fields = ('no', 'datefrom', 'datedue',)

class    OrgInsuranceForm(forms.ModelForm):
    date        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата договора')
    datefrom    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Страховка с', required=False)
    datedue        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Страховка по', required=False)
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = OrgInsurance
        fields = ('insurer', 'no', 'date', 'sum', 'datefrom', 'datedue', 'active')
###(1
class    OrgPhoneForm(forms.ModelForm):
    class    Meta:
        model = ContactPhone
        fields = ('phone',)

class    OrgEmailForm(forms.ModelForm):
    class    Meta:
        model = ContactEmail
        fields = ('email',)

class    OrgWWWForm(forms.ModelForm):
    class    Meta:
        model = ContactWWW
        fields = ('www',)
###1)
class    OrgStuffForm(forms.ModelForm):
    person       = forms.ModelChoiceField(queryset=Person.objects.all(), empty_label=None)
    role         = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None)
    startdate    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата принятия', required=False)

    class    Meta:
        model = OrgStuff
        fields = ('person', 'role', 'leader', 'permanent', 'startdate')

class    OrgStuffForm_Soft(forms.Form):
    person      = forms.ModelChoiceField(queryset=Person.objects.all(), empty_label=None)
    role        = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None)
    leader      = forms.BooleanField()
    permanent   = forms.BooleanField()
    startdate   = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата принятия')
    person.widget.attrs["onchange"]="getRole()"
    def    __init__(self, org, *args, **kwargs):
        super(OrgStuffForm_Soft, self).__init__(*args, **kwargs)
        self.fields['person'].queryset = Person.objects.exclude(id__in=org.orgstuff_set.values_list('person'))
    #class    Meta:        model = OrgStuff;;; fields = ('person', 'role', 'leader', 'permanent')
        
class    OrgStuffAddPersonForm(forms.ModelForm):
    class    Meta:
        model = Person
        fields = ('firstname', 'midname', 'lastname')

class    OrgStuffAddRoleForm(forms.ModelForm):
    class    Meta:
        model = Role

#class    StageListListForm(forms.Form):
#    type    = forms.ModelChoiceField(queryset=StageListType.objects.all(), required=False, empty_label=None)

class    StatementForm(forms.ModelForm):
    date    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата')

    class    Meta:
        model = Statement
        fields = ('date','rejectprotocol')    # FIXME: publish

class    PermitForm(forms.ModelForm):
    date        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата')

    def    setdata(self, orgsro):
        self.fields['protocol'].queryset = Protocol.objects.filter(sro=orgsro.sro,type=0)
        self.fields['statement'].queryset = Statement.objects.filter(orgsro=orgsro)

    class    Meta:
        model = Permit
        #fields = ('no', 'date', 'protocol')    # FIXME: publish
        fields = ('no', 'date', 'protocol', 'statement')    # FIXME: publish

class ProtocolListForm(forms.Form):
    protocol    = forms.ModelChoiceField(queryset=Protocol.objects.all(), label='Протокол-основание')
    def    setdata(self, orgsro):
        self.fields['protocol'].queryset = Protocol.objects.filter(sro=orgsro.sro).exclude(type=1)
    def    setdataD(self, orgsro):
        self.fields['protocol'].queryset = Protocol.objects.filter(sro=orgsro.sro,type=1)

class    StatementAddForm(forms.Form):
    ver    = forms.ModelChoiceField(queryset=StageVer.objects.all(), label='Версия')
    date    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата')


class PermitListForm(forms.Form):
    permit = forms.ModelChoiceField(queryset=Permit.objects.all(), label='Свидетельство')
    def    setdata(self, orgsro):
        self.fields['permit'].queryset = Permit.objects.filter(orgsro=orgsro,statement__isnull=True,status=0)


class    PermitAddForm(forms.Form):
    ver        = forms.ModelChoiceField(queryset=StageVer.objects.all(), label='Версия')
    no        = forms.CharField(max_length=50, label='Номер свидетельства')
    date        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата')
    protocol    = forms.ModelChoiceField(queryset=Protocol.objects.all(), required=False, label='Протокол')
    statement    = forms.ModelChoiceField(queryset=Statement.objects.all(), required=False, label='Заявление')
    error_css_class = 'error'
    required_css_class = 'required'

    def    setdata(self, orgsro):
        self.fields['protocol'].queryset = Protocol.objects.filter(sro=orgsro.sro,type=0)
        self.fields['statement'].queryset = Statement.objects.filter(orgsro=orgsro)

class    CompareToForm(forms.Form):
    other    = forms.ModelChoiceField(queryset=None, empty_label=None)
    def    __init__(self, stagelist, *args, **kwargs):
        super(CompareToForm, self).__init__(*args, **kwargs)
        self.fields['other'].queryset = stagelist.orgsro.stagelist_set.exclude(pk=stagelist.id)

class    PersonMainForm(forms.ModelForm):
    class    Meta:
        model = Person
        fields = ('lastname', 'firstname', 'midname')

class    PersonSkillForm(forms.ModelForm):
    skilldate    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'Дата окончания', required=False)
    seniodate    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'Дата актуальности стажа', required=False)
    tested        = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'Аттестат. Дата выдачи', required=False)
    #coursedate    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'СоПК. Дата выдачи', required=False)
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = PersonSkill
        fields = ('speciality', 'skill', 'skilldate', 'school', 'seniority', 'seniodate', 'tested')

class    PersonSkillAddSpecialityForm(forms.ModelForm):
    class    Meta:
        model = Speciality
        fields = ('name',)

class    PersonSkillAddSkillForm(forms.ModelForm):
    class    Meta:
        model = Skill

class    CourseForm(forms.ModelForm):
    coursedate    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label=u'СоПК. Дата выдачи', required=True)
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = Course
        fields = ('courseno', 'coursedate', 'coursename', 'courseschool')

#class    PDFSelectForm(forms.Form):
#    title    = forms.BooleanField(label='Титул', initial=True, required=False)
#    stages    = forms.BooleanField(label='Работы', initial=True, required=False)

class    ProtocolMainForm(forms.ModelForm):
    date    = forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата протокола')
    type = forms.ChoiceField(choices=[(0, "Протокол Заседания Правления"),
                                         (1, "Протокол Дисциплинарной Коммисии"),(2, "Протокол Общего Собрания")], label='Тип протокола')
    class    Meta:
        model = Protocol
        fields = ('no', 'date','type')
