* +DB struct change:
	* +core.models.FileSeqItem.file: PrimaryKey
	* +scan.model.Scan.events: json?
	* +bills.model.Bill.fileseq: FK => 1-2-1 PrimaryKey
	* +bills.model.Route.state: delete
	* +bills.model.Route.action: delete
	* +bills.model.State: delete
* Route templates
* Вынести прибитую гвоздями логику в плагины
* Добавление/удалений файлов в счете
* Place/Subject subsystem
* Chat
* Interface:
	* bill list:
		* фильтр состояний - в колонку
		* вся строка == URL
	* bill detail:
		* dynamic Subject
		* Камменты - 1 строка
		* раскрасить как-нить
		* Preview переделать
* Security:
	* https
	* session timeout
	* logging?
* fixtures (JSON, w/ auth.user)
* unittests
* django 1.5?
* pyhon3?
* MySQL
