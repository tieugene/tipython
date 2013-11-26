= DB =

== lang ==
(predefined)
* code:ch(2) - ISO 639-1
* name (ru)

== genre ==
(pedefined)

=== theme ===
* name (ru)

=== genre ===
* code
* name (ru)

== author ==
*
* pedivikia URL
* author home url
* email?
* ids (in libs)

== book ==
* <series>
* md5
* size
* checked (lang, genre, author, ids)
* author (m:m)
* ids (in libs)

== library ==
* name (lib.rus.ec, flibusta.net, coollib.net, traumlibrary.net)
* home_url
* author_url
* book_url

= Parsing =

== lang ==
title-info/lang
Если совпадает - назначается. Если нет - и суда нет.

== genre ==
title-info/genre - _первый_ из них
Если совпадает - назначается. Если нет - и суда нет.

== author ==

== book ==

= Notes =
* merge w/ checked only
* checked == all fields are correct
* Author == Person|Org