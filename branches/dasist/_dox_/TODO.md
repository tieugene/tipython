!!! План работы и смета !!!

Смета:
	* 0.0.3 + конвертер

= 2014-05-06 =
+ Суммы - с копейками
* Комментарий к action - длиннее
+ place, subject, depart - order by name
+ Иконку фильтра - справа
+ В список: плательщик, сумма к оплате
+ Сканы - исправить колонки
+ Контроль сумм при вводе
+ При оплате - пересчет сумм
* Состояния: доплата
* Дубли:
** мылом реквизиты и историю - гендиру + Завернуть
** контроль Номер+Дата+СуммаСчета
* Список счетов: Фильтр: Направление, Поставщик, Исполнитель
* Педаль "Печать" (бухгалтеру)
* Добавление файлов в счет

== контроль сумм ==
* Сумма счета - 0
* Оплачено > СуммыСчета
* К оплате > (Сумма-Оплачено)

= 0.1.0 =

== Hot ==
* +DB struct change:
	* +core.models.FileSeqItem.file: PrimaryKey
	* +scan.model.Scan.events: json?
	* +bills.model.Bill.fileseq: FK => 1-2-1 PrimaryKey
	* +bills.model.Route.state: delete
	* +bills.model.Route.action: delete
	* +bills.model.State: delete
* +Place=>Subject dynafilter
* +summs
* +remake Scan
* +fixtures (JSON, w/ auth.user)
* +0.0.3=>0.1.0 converter

= 0.1.1 =
* scan.even => scan.comments

== Lazy ==
* Tunes:
	* Security:
		* views
		* https
		* session timeout
		* logging?
	* Perfomance:
		* Limit CharFields widths
		* MySQL
		* 304
	* Visibility:
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
			* +dynamic Subject
			* +1-line comments
			* fonts/sizes/colors/formsets
			* Preview remake
		* bill edit:
			* limit Supplier (width, CAPS)
	* Usability:
		* <2B continued>
	* Supportability:
		* CSS
* Place/Subject subsystem
* Add/del images in fileseq

= 0.0.X =
* new state machine
** move hardcoded logic into "plugins"
* Route templates
* Chat

= Future =
* django 1.5?
* pyhon3?
* unittests

= misc =
http://habrahabr.ru/post/220295/