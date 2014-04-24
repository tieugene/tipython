* +DB struct change:
	* +core.models.FileSeqItem.file: PrimaryKey
	* +scan.model.Scan.events: json?
	* +bills.model.Bill.fileseq: FK => 1-2-1 PrimaryKey
	* +bills.model.Route.state: delete
	* +bills.model.Route.action: delete
	* +bills.model.State: delete
* Place=>Subject dynafilter
* Route templates
* Вынести прибитую гвоздями логику в плагины
* Place/Subject subsystem
* Security:
	* views
	* https
	* session timeout
	* logging?
* Добавление/удалений файлов в счете
* Chat
* Interface:
	* CSS
	* Till 1024 width
	* disable ALLCAPS words in Supplier
	* bill list:
		* фильтр состояний - в колонку
		* брехня... фильтр состояний - 5 педалек с JS (!)
		* вся строка == URL
		* select columns to view
		* state as icon
		* nowrap
	* bill detail:
		* dynamic Subject
		* Камменты - 1 строка
		* раскрасить как-нить
		* Preview переделать
	* bill edit:
		* ограничить Поставщика (длина, капс)
* fixtures (JSON, w/ auth.user)
* unittests
* django 1.5?
* MySQL
* pyhon3?
http://habrahabr.ru/post/220295/