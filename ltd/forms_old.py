class	DocTypeForm(forms.ModelForm):
	class	Meta:
		model = DocType

class	DocEntityForm(forms.ModelForm):
	class	Meta:
		model = DocEntity

class	DocForm_0001(forms.Form):
    #name	= forms.CharField(label='Наименование фирмы (кратко)', help_text='пример: Ромашко')
    #fss_no	= forms.IntegerField(label='Филиал ФСС №:')
    #opening	= forms.BooleanField(label='Открытие:', required=False)
    #oname	= forms.CharField(label='Наименование фирмы (полное)', help_text='пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»')
    #oinn	= forms.CharField(label='ИНН фирмы', min_length=10, max_length=12)
    #okpp	= forms.CharField(label='КПП фирмы', min_length=9, max_length=9)
    #ookato	= forms.CharField(label='ОКАТО фирмы', min_length=8, max_length=11)
    #oogrn	= forms.CharField(label='Рег. №', min_length=10, max_length=16, help_text='ОГРН, штоле?')
    #bname	= forms.CharField(label='Полное наименование банка', help_text='пример: Открытое акционерное общество «Санкт-Петербургский Индустриальный Акционерный Банк»')
    #binn	= forms.CharField(label='ИНН банка', min_length=10, max_length=12)
    #bkpp	= forms.CharField(label='КПП банка', min_length=9, max_length=9)
    #bogrn	= forms.CharField(label='ОГРН банка', min_length=10, max_length=16)
    #bik	= forms.CharField(label='БИК', min_length=9, max_length=9)
    #rs		= forms.CharField(label='Р/с', min_length=20, max_length=20)
    #jobrole	= forms.CharField(label='Руководитель.Должность', min_length=4, max_length=20, help_text='пример: Ген. директор')
    #boss	= forms.CharField(label='Руководитель.Фамилия И. О.', min_length=4, max_length=64, help_text='пример: Иванов И. И.')
    #date0	= forms.DateField(label='Дата закрытия/открытия', help_text='пример: 27.09.2011')
    #date1	= forms.DateField(label='Дата документа')


class	DocForm_0002(forms.Form):
    #name	= forms.CharField(label='Наименование фирмы (кратко)', help_text='пример: Ромашко')
    #opening	= forms.BooleanField(label='Открытие:', required=False)
    #oname	= forms.CharField(label='Наименование фирмы (полное)', help_text='пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»')
    #oaddr	= forms.CharField(label='Адрес фирмы', help_text='пример: 191187, Санкт-Петербург, ул. Шпалерная, д. 9, литер А, пом. 4-Н')
    #oinn	= forms.CharField(label='ИНН фирмы', min_length=10, max_length=12)
    #opfrno	= forms.CharField(label='Рег. № в ПФР', min_length=14, max_length=14)
    #opfrname	= forms.CharField(label='УПФР в', help_text='пример: Центральном р-не г. Санкт-Петербурга')
    #bname	= forms.CharField(label='Полное наименование банка', help_text='пример: Открытое акционерное общество «Санкт-Петербургский Индустриальный Акционерный Банк»')
    #baddr	= forms.CharField(label='Адрес банка')
    #binn	= forms.CharField(label='ИНН банка', min_length=10, max_length=12)
    #bkpp	= forms.CharField(label='КПП банка', min_length=9, max_length=9)
    #bik	= forms.CharField(label='БИК', min_length=9, max_length=9)
    #rs		= forms.CharField(label='Р/с', min_length=20, max_length=20)
    #jobrole	= forms.CharField(label='Руководитель.Должность', min_length=4, max_length=20, help_text='пример: Ген. директор')
    #boss	= forms.CharField(label='Руководитель.Фамилия И. О.', min_length=4, max_length=64, help_text='пример: Иванов И. И.')
    #date0	= forms.DateField(label='Дата закрытия/открытия', help_text='пример: 27.09.2011')
    #date1	= forms.DateField(label='Дата документа')

class	DocForm_0003(forms.Form):
    #name	= forms.CharField(label='Наименование фирмы (кратко)', help_text='пример: Ромашко')
    #opening	= forms.BooleanField(label='Открытие:', required=False)
    #kno	= forms.CharField(label='Код налогового органа', min_length=4, max_length=4)
    #otype	= forms.ChoiceField(label='Тип фирмы', choices=(('1', 'Российская'), ('2', 'Иностранная'), ('3', 'Иностранная через ОП'), ('4', 'ИП'), ('5', 'Нотариус')))
    #oname	= forms.CharField(label='Наименование фирмы (полное)', help_text='пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»')
    #oinn	= forms.CharField(label='ИНН фирмы', min_length=10, max_length=12)
    #okpp	= forms.CharField(label='КПП фирмы', min_length=9, max_length=9)
    #oogrn	= forms.CharField(label='ОГРН фирмы', min_length=10, max_length=16)
    #jobrole	= forms.CharField(label='Руководитель.Должность', min_length=4, max_length=20, help_text='пример: Ген. директор')
    #bossf	= forms.CharField(label='Фамилия руководителя', min_length=4, max_length=20)
    #bossi	= forms.CharField(label='Имя руководителя', min_length=4, max_length=20)
    #bosso	= forms.CharField(label='Отчество руководителя', min_length=4, max_length=20)
    #bossinn	= forms.CharField(label='ИНН руководителя', min_length=10, max_length=12)
    #bossphone	= forms.CharField(label='Контактный телефон руководителя', min_length=6, max_length=20)
    #rs		= forms.CharField(label='Счёт', min_length=20, max_length=20)
    #oogrnip	= forms.CharField(label='ОГРНИП')
    ##kio 	= forms.CharField(label='КИО')
    #bname	= forms.CharField(label='Полное наименование банка', help_text='пример: Открытое акционерное общество «Санкт-Петербургский Индустриальный Акционерный Банк»')
    #binn	= forms.CharField(label='ИНН банка', min_length=10, max_length=12)
    #bkpp	= forms.CharField(label='КПП банка', min_length=9, max_length=9)
    #bzip	= forms.CharField(label='Индекс банка', min_length=6, max_length=6)
    #breg	= forms.CharField(label='Код региона', min_length=1, max_length=2)
    #bik	= forms.CharField(label='БИК', min_length=9, max_length=9)
    #badistr	= forms.CharField(label='Адрес банка: район', required=False)
    #batown	= forms.CharField(label='Адрес банка: город')
    #bapunkt	= forms.CharField(label='Адрес банка: населённый пункт', required=False)
    #bastreet	= forms.CharField(label='Адрес банка: улица (проспект, переулок и т.д.)')
    #bahouse	= forms.CharField(label='Адрес банка: номер дома (владения)')
    #bastr	= forms.CharField(label='Адрес банка: номер корпуса (строения)', required=False)
    #baoff	= forms.CharField(label='Адрес банка: номер офиса', required=False)
    #date0	= forms.DateField(label='Дата закрытия/открытия', help_text='пример: 27.09.2011')
    #date1	= forms.DateField(label='Дата документа')

class	DocForm_0004(forms.Form):
	name		= forms.CharField(label='Наименование фирмы (кратко)', help_text='пример: Ромашко')
	#fname		= forms.CharField(label='Полное наименование', help_text='пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»')
	#sname		= forms.CharField(label='Сокращенное наименование', help_text='пример: ООО «ТД Ромашко»')
	#f_fname	= forms.CharField(label='Полное наименование на иностранном языке', required=False, help_text='пример: «Trade house Romashko»')
	#f_sname	= forms.CharField(label='Краткое наименование на иностранном языке', required=False, help_text='пример: «ТH Romashko»')
	#f_lang		= forms.CharField(label='Иностранный язык в предложном падеже', required=False, help_text='пример: английском')
	inidoc_n	= forms.IntegerField(label='Решение: №', required=False)
	inidoc_d	= forms.DateField(label='Решение: дата', required=False)
	inidoc_p	= forms.CharField(label='Решение: место', required=False)
	boss_f		= forms.CharField(label='Генеральный директор: фамилия', required=False)
	boss_i		= forms.CharField(label='Генеральный директор: имя', required=False)
	boss_o		= forms.CharField(label='Генеральный директор: отчество', required=False)
	boss_r		= forms.CharField(label='Генеральный директор: ФИО в родительном падеже', required=False)
	boss_d		= forms.CharField(label='Генеральный директор: фамилия в дательном падеже', required=False)
	boss_sp		= forms.IntegerField(label='Генеральный директор: серия паспорта', required=False)
	boss_np		= forms.IntegerField(label='Генеральный директор: номер паспорта', required=False)
	boss_p		= forms.CharField(label='Генеральный директор: паспорт выдан', required=False)
	boss_a		= forms.CharField(label='Генеральный директор: адрес', required=False)
	mifns_no	= forms.CharField(label='МИ ФНС №', required=False, help_text='пример: 15 по Санкт-Петербургу')
	address		= forms.CharField(label='Адрес', required=False)
	addr_zip	= forms.CharField(label='Адрес: индекс', required=False, help_text='пример: 192001')
	#addr_srf	= forms.CharField(label='Адрес: субъект РФ', required=False, help_text='пример: г.Санкт-Петербург')
	#addr_reg	= forms.CharField(label='Адрес: район', required=False)
	#addr_cty	= forms.CharField(label='Адрес: город', required=False)
	#addr_twn	= forms.CharField(label='Адрес: населенный пункт', required=False)
	#addr_str	= forms.CharField(label='Адрес: улица', required=False, help_text='(проспект, переулок и т.п. - нужное указать)')
	#addr_hse_t	= forms.CharField(label='Адрес: дом', required=False, help_text='(владение и т.п. - нужное указать)')
	#addr_hse_n	= forms.CharField(label='Адрес: номер дома', required=False)
	#addr_bld_t	= forms.CharField(label='Адрес: корпус', required=False, help_text='(строение и т.п. - нужное указать)')
	#addr_bld_n	= forms.CharField(label='Адрес: номер корпуса', required=False)
	#addr_app_t	= forms.CharField(label='Адрес: квартира', required=False, help_text='(офис и т.п. - нужное указать)')
	#addr_app_n	= forms.CharField(label='Адрес: номер квартиры', required=False)
	capital		= forms.CharField(label='Размер уставного капитала', required=False, help_text='пример: 10000')
	capital_p	= forms.CharField(label='Размер уставного капитала прописью', required=False, help_text='пример: десять тысяч')
