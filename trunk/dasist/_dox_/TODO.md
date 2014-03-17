= 2014-03-09 =
== Bills ==
+ create users
+ CRUD bill
* route bill
* permissions
* FIXME:
	* files not deleted:
		https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.pre_delete
		http://stackoverflow.com/questions/2747118/django-deleting-models-and-overriding-delete-method
	* list: state
	* list: can*
	* list: filter
	* view: state
	* view: can
	* view: download image
	* convert: PDF
	* convert: tiff not deleted
	* ерунда с этим done и rpoint получается...
	* обязательность камментов - в форме

States (list):
* Draft: done=None, rpoint=None
* OnWay: done=None, rpoint!=None
* Accepted: done=True
* Rejected: done=False

FIXME:
* Approver.user == PK

====
Fixme:
* form: add/edit header and cancel

Feature:
* Check route (user can't be in route, end must be accounter)
* Check note on reject
* Filters (state & user; view bill by intermediate approver)
* Project and Depart as models (?)
* mailto
* preview
* перехват счетов в пути
* Перезапуск несогласованного счет
* Archive

Tuning:
* colorify (lightgrey/white, yellow, green, red)
* paging
* зачеркивать пройденный маршрут
* login=>ФИО+должность
* users in groups

Future:
* thunderbird-lightning.Tasks
* webp

= 2014-02-21 =
* Всем - ФИО
* Окончание маршрута - на егоровой
* + птица "оплачено"
* Перезапуск == в черновик (с историей)
* Обязательно:
0.
1. Аня (если не Исполнитель)
2. Руководители направлений
3. Борщенко (юрист)/Константинов (исполдир)/Геннадий (техдир) (один из них)
4. НВ
5. Главбух

?. Горелов и завьялов

----
Получается схема:
1. один из манагер ОМТС - опция
2. один РукОМТС - обязательно
3. один из РукНапр - обязательно
4. любой из Директоров - обязательно
5. один ГенДир - обязательно (согласован)
6. один ГлавБух - обязательно

Итого ролей: 6


Да и счет - это последовательность grey/bw png

Format-specific tools:
optipng.i686 : PNG optimizer and converter (optipng)
pngcrush.i686 : Optimizer for PNG (Portable Network Graphics) files (pngcrush)
gif2png

----
* File => ImgFile => PNGFile
* PNGSet/FileSequence
* splitconvertimage (to bw/grey)