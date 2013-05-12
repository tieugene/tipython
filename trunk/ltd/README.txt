= Links =
* http://dik123.blogspot.com/2010/06/pdf.html

= Requirements =
* python-pytils
* python-pymorphy
* python-wkhtmltopdf
* python-webodt
* wkhtmltopdf
* unoconv

= Thoughts =
* selected refs:
	* okved
	* субъект федерации
* selected forms:
	* fio (учредители)
	* addr (орг, гендир, учредител
	* документ
	* 
= Prereq: =
	* ООО
	* с нуля
	* Master\public\Юридический отдел\РЕГИСТРАЦИЯ
1. Решение:
	* номер, дата, место
	* ФИО
	* документ (тип, серия, номер, выдан (кем, когда (полностью), код подразделения)
	* Зарегистрирован по адресу, РФ, индекс, субъект, итд
	* место нахождения
2. Устав:
	* полное фирменное наименование (в кавычках) - req
	* краткое фирменное наименование (в кавычках) - req
	* полное на иностранном языке - язык в предложном падеже ("английском"), название - option
	* краткое - option
	* индекс - req
	* Адрес: субъект федерации, улица/проспект etc, дом etc - req
	* кол-во учредителей
3. Заявление на УСН:
	* номер инспекции
4. Форма 1101:
	* 
5. Квитанция1:
6. Доверка ???
7. Опись:
8. Приказ #1:
	* дата
9. Проклейки:
10. Квитанция2:
11. Заявление на выдачу копии
12. Доверка №2:
13. Письмо в ПФР
14. Копия списка участников

= Solution =
* data stored in json (json<>dict; save/load)
* sqlite
* data: name (from data), comments?, data
* maybe - address and FIO - sepparately
* formset?

= Menu =
* Doc
* Logout

= Actions =
* List
* Detail:
	* Add
	* Copy to
	* Edit
	* Del
	* View
	* Preview
	* Print (PDF)

= Future =
* Address
* FIO, address, doc
* Org
* History (user, created/updated)
* Permissions

= Libs =
* ODT: django-webodt
* PDF: PISA, django-pdf, xhtml2pdf
* 

= Req =

* django-webodt python-lxml libreoffice-xsltfilter

*  OBS: django-xhtml2pdf
*  OBS: xhtml2pdf (https://github.com/chrisglass/xhtml2pdf) - git
** python-reportlab
** pyPdf
** PIL
** +OBS: html5lib (http://code.google.com/p/html5lib/) - mercurial (hg)
* python-trml2pdf
** python-reportlab
