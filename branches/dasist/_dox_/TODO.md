= 0.0.3 =

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
* fixtures (JSON, w/ auth.user)
* 0.0.2=>0.0.3 converter

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