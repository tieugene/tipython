# 0.1.0
* Dups - mailto TheBoss bill requisitions and history ([HowTo]((http://stackoverflow.com/questions/882712/sending-html-email-using-python HowTo))
- Bug: partialy payed stay Drtaft? (6) but not Done? (9) (e.g. 957)

# 0.1.1

Usability:

+ Action comment string must be longer
* Bill list: Filter: Depart, Supplier, Assignee
* "Print" button (4 Accounter)
* Place/Subject subsystem
* Add/del images in fileseq
* 1024x768
* bill list:
  * states filter == X x buttons:
    * Draft: "draft" (Edit)
    * OnWay: onway
    * OnPay: $
    * Done: V
    * Rejected: Trash
    * +JS (Ajax)
 * tr == URL
 * ?select columns to view
 * state as icon:
	* Draft: new/edit
	* OnWay: man
	* OnPay: $
	* Done: v
	* Reject: trash
 * ?nowrap
* fonts/sizes/colors
* bill detail: formsets
* Img preview remake
* bill edit: limit Supplier (width, CAPS)

# 0.1.2

Reliability:

* views prerequisites (ACL)
* transactions
* Uniq billno&billdate&billsum

# 0.1.3

Security:

* https
? session timeout
* logging?

# 0.1.4

Perfomance:

* Limit CharFields widths
* MySQL
* 304

# 0.1.5

Supportability:

* CSS
* unittests
* One way ticket (?)

# 0.1.X

Expandability:

* ? scan.even => scan.comments
* move hardcoded logic into "plugins"
* Route templates
* Chat
* django 1.5?
* ?pyhon3

# 0.1.Y

* ?History - replace Y/N (bool) with "next state"

# 0.1.Z

Scans:

* Filters:
	* Place
	* Subject
	* Depart
	* -Assignee
* Search:
	* Supplier
	* Billno
	* Billdate
