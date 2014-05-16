!!! План работы и смета !!!

= Test =
+Draft > Edit > Delete
+Draft > OnWay > Reject > Delete
+Draft > OnWay > Reject > Draft >
+Draft > OnWay > OnPay > Done
+Draft > OnWay > OnPay > Dup
+Draft > OnWay > OnPay > Done? > +Draft? > Edit > Draft? > OnWay? > Reject? > Draft? > OnWay? > OnPay > Done

= 0.1.0 =
2014-05-06:
+ 0.0.3 + конвертер
+ Суммы - с копейками
+ place, subject, depart - order by name
+ Иконку фильтра - справа
+ В список: плательщик, сумма к оплате
+ Сканы - исправить колонки
+ Контроль сумм при вводе:
++ Сумма счета - 0
++ Оплачено > СуммыСчета
++ К оплате > (Сумма-Оплачено)
+ При оплате - пересчет сумм
+ Состояния: доплата
+ new state machine
+ bill_edit (restarated)
* Дубли:
++ Завернуть
** мылом реквизиты и историю - гендиру
* to scan

= 0.1.1 =
Tuning:
* Список счетов: Фильтр: Направление, Поставщик, Исполнитель
* Педаль "Печать" (бухгалтеру)
* Добавление файлов в счет
* Комментарий к action - длиннее
* Place/Subject subsystem
* Add/del images in fileseq
? scan.even => scan.comments
* контроль Номер+Дата+СуммаСчета

= 0.1.2 =
Visibility:
* 1024x768
* bill list:
	* states filter == X x buttons:
		* Draft: "draft" (Edit)
		* OnWay: onway
		* OnPay: $
		* Done: V
		* Rejected: Trash
		* +JS
	* tr == URL
	* select columns to view (?)
	* state as icon
	* nowrap
* bill detail:
	* fonts/sizes/colors/formsets
	* Preview remake
* bill edit:
	* limit Supplier (width, CAPS)

= 0.1.3 =
Security:
* views
* https
* session timeout
* logging?

= 0.1.4 =
Perfomance:
* Limit CharFields widths
* MySQL
* 304

= 0.1.5 =
Supportability:
* CSS
* unittests
* One way ticket

= 0.1.X =
** move hardcoded logic into "plugins"
* Route templates
* Chat

= 0.1.Y =
* django 1.5?
* pyhon3?
* unittests

= browsers =
+ firefox
+ qupzilla
+ chrome
+ rekonq
+ konqueror
+ opera
+ arora
* epiphany
* dwb
+ midori
* kazehakase
* kazehakase-webkit
+ Mosaic
