"""
invoice.forms
"""
# 1. sys
import decimal
# 2. django
from django import forms
from django.db.models.fields.files import FieldFile
# 3. 3rd
from dal import autocomplete
# 4. local
from contrib.models import Org, Department, Payer, Place, Subject, Bank
from contract.models import Contract
from contrib.forms import InnField, chk_new_org, chk_org_names
from .models import Invoice

mime_available = {
    'image/png',
    'image/tiff',
    'image/jpeg',
    'application/pdf',
}


# class ApproverModelChoiceField(forms.ModelChoiceField):
#    def label_from_instance(self, obj):
#        return obj.get_fio()


class ResumeForm(forms.Form):
    note = forms.CharField(max_length=255, label='Comments', required=False, widget=forms.TextInput(attrs={'size': 80}))


class FilterInvoiceListForm(forms.Form):
    draft = forms.BooleanField(label='Draft', required=False)
    onway = forms.BooleanField(label='On way', required=False)
    onpay = forms.BooleanField(label='On pay', required=False)
    done = forms.BooleanField(label='Complete', required=False)
    dead = forms.BooleanField(label='Rejected', required=False)
    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), label='Договор', required=False)
    bank = forms.ModelChoiceField(queryset=Bank.objects.all().order_by('name'), label='Банк', required=False)
    shipper = forms.ModelChoiceField(queryset=Org.objects.all(), label='Поставщик', required=False, widget=autocomplete.ModelSelect2(url='org-autocomplete'))

    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        # None or unicode/int
        # place = self.fields['place'].initial or self.initial.get('place') or self._raw_value('place')
        place = self.fields['place'].initial or self.initial.get('place')
        if place:
            # parent is known. Now I can display the matching children.
            self.fields['subject'].queryset = Subject.objects.filter(place__pk=int(place)).order_by('name')


class InvoiceAddFileForm(forms.Form):
    file = forms.FileField(label='Файл')
    rawpdf = forms.BooleanField(label='Конвертировать PDF', required=False)

    def clean_file(self):
        file = self.cleaned_data['file']
        if (not isinstance(file, FieldFile)) and (file.content_type not in mime_available):
            raise forms.ValidationError('File must be PNG, TIF, JPG or PDF!')
        return None


class InvoiceForm(forms.Form):
    """
    Parent form; abstract only.
    """
    file = forms.FileField(label=u'Скан')
    rawpdf = forms.BooleanField(label=u'Конвертировать PDF', required=False)
    place = forms.ModelChoiceField(queryset=Place.objects.all().order_by('name'), empty_label=None, label='Объект')
    bank = forms.ModelChoiceField(queryset=Bank.objects.all().order_by('name'), empty_label='---', label='Плательщик')
    suppinn = InnField(min_length=10, max_length=12, label='ИНН Поставщика', required=True)
    suppname = forms.CharField(max_length=64, label='Поставщик (кратко)', required=True)
    suppfull = forms.CharField(max_length=64, label='Поставщик (полностью)', required=True)
    doc_no = forms.CharField(max_length=64, label='Номер счета')
    doc_date = forms.DateField(label=u'Дата счета')
    doc_sum = forms.DecimalField(max_digits=11, decimal_places=2, min_value=decimal.Decimal('0.01'), localize=True, label=u'Сумма счета')
    sum_payed = forms.DecimalField(max_digits=11, decimal_places=2, min_value=decimal.Decimal('0.00'), localize=True, label=u'Оплачено')
    sum_2pay = forms.DecimalField(max_digits=11, decimal_places=2, min_value=decimal.Decimal('0.00'), localize=True, label=u'Сумма к оплате')
    # mgr = ApproverModelChoiceField(queryset=Approver.objects.filter(role__pk=3), empty_label=None, label=u'Руководитель', widget=forms.RadioSelect)
    # # boss = ApproverModelChoiceField(queryset=Approver.objects.filter(role__pk=5), empty_label=None, label=u'Гендиректор', widget=forms.RadioSelect)

    def clean(self):
        cleaned_data = super(BillForm, self).clean()
        # 1. chk inn<>suppname
        suppinn = cleaned_data.get('suppinn')
        suppname = cleaned_data.get('suppname')
        suppfull = cleaned_data.get('suppfull')
        if suppinn and suppname:
            chk_new_org(suppinn, suppname)
        # 2. chk supp names
        if suppname and suppfull:
            chk_org_names(suppname, suppfull)
        # 3. chk summs
        doc_sum = cleaned_data.get('doc_sum')
        sum_payed = cleaned_data.get('sum_payed')
        sum_2pay = cleaned_data.get('sum_2pay')
        if doc_sum is None:
            raise forms.ValidationError('Заполните сумму счета.')
        if sum_payed is None:
            raise forms.ValidationError('Заполните Оплачено.')
        if sum_payed > doc_sum:
            raise forms.ValidationError('Оплачено больше суммы счета.')
        if sum_2pay is None:
            raise forms.ValidationError('Заполните сумму к оплате.')
        if sum_2pay > (doc_sum - sum_payed):
            raise forms.ValidationError('К оплате больше чем надо.')
        return cleaned_data


class InvoiceAddForm(InvoiceForm):
    """
    Add new bill
    """
    def clean_file(self):
        file = self.cleaned_data['file']
        if (not isinstance(file, FieldFile)) and (file.content_type not in mime_available):
            raise forms.ValidationError('File must be PNG, TIF, JPG or PDF!')
        return None

    def clean(self):
        cleaned_data = super(BillAddForm, self).clean()
        # 4. chk unqueness
        shipper__inn = cleaned_data.get('suppinn')
        billno = cleaned_data.get('doc_no')
        billdate = cleaned_data.get('doc_date')
        if shipper__inn and doc_no and doc_date:
            if Invoice.objects.filter(
                shipper__inn=shipper__inn,
                doc_no=doc_no,
                doc_date=doc_date
            ).exists():
                raise forms.ValidationError('Такой счет уже есть.')
        return cleaned_data


class InvoiceEditForm(InvoiceForm):
    """
    Edit existance invoice (not locked)
    """
    id = forms.IntegerField(label='ID', widget=forms.HiddenInput())
    file = forms.FileField(label='Скан', required=False, help_text='(Выберите файл, если хотите заменить скан)')

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            if (not isinstance(file, FieldFile)) and (file.content_type not in mime_available):
                raise forms.ValidationError('File must be PNG, TIF, JPG or PDF!')
        return None

    def clean(self):
        cleaned_data = super(BillEditForm, self).clean()
        # 4. chk unqueness
        if Invoice.objects.filter(
            shipper__inn=cleaned_data['suppinn'],
            doc_no=cleaned_data['doc_no'],
            doc_date=cleaned_data['doc_date']
        ).exclude(fileseq_id=int(cleaned_data['id'])).exists():
            raise forms.ValidationError('Такой счет уже есть.')
        return cleaned_data


class InvoiceReEditForm(forms.Form):
    """
    Edit locked invoice
    """
    sum_2pay = forms.DecimalField(max_digits=11, decimal_places=2, min_value=decimal.Decimal('0.01'), localize=True, label=u'Сумма к оплате')
    # mgr = ApproverModelChoiceField(queryset=Approver.objects.filter(role__pk=3), empty_label=None, label=u'Руководитель', widget=forms.RadioSelect)
    # boss = ApproverModelChoiceField(queryset=Approver.objects.filter(role__pk=5), empty_label=None, label=u'Гендиректор', widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        if 'max_topaysum' in kwargs:
            self.max_topaysum = kwargs.pop('max_sum_2pay')
        else:
            self.max_topaysum = None
        super(InvoiceReEditForm, self).__init__(*args, **kwargs)

    def clean_topaysum(self):
        topaysum = self.cleaned_data['sum_2pay']
        if self.max_topaysum:
            if topaysum > self.max_topaysum:
                raise forms.ValidationError('Больше %s не дадут' % self.max_topaysum)
        return topaysum
