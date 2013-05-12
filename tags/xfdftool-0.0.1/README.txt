+ 1. show form fields
+ 2. export xfdf (FdfWriter) - FDF only
  3. export xdp - handwriting (or further)
+ 4. populate form w/ data (AcroForm) > flatten
+ 5. populate form w/ data (XFA) > flatten
+ 6. populate form w/ xfdf - (AcroForm = ASCII, XFA - OK (full field names))
  7. All together:
	* list form fields (input.pdf > stdout) - radio/choice values (http://itextpdf.com/examples/iia.php?id=121)
	* export XFDF/XDP template (input.pdf > stdout)
	* fill form w/ XFDF/XDP file (input.pdf data.xfdf/stdin)
  X. Convert xdp/xml to xfdf

URLs:
	* XFA: http://itext-general.2136553.n4.nabble.com/Can-t-read-Acro-XFA-fields-after-offline-saving-td2158752.html
	* XfdfFill: http://dik123.blogspot.com/2010/06/pdf.html
	* ant: http://www.opennet.ru/base/dev/ant_10.txt.html
====
Syntax (2..4 arguments):
	xfdftool <option> <form.pdf> [-o output] [-i input]
Options:
	* -i - info
		xfdftool -i <form.pdf> [output.txt/-]
	* -l/L - list fields / ... - short names
		xfdftool -l/L <form.pdf> [output.txt/-]
	* -e/E - export xfdf form / ... - short names
		xfdftool -e/E <form.pdf> [output.xfdf/-]
	* -f/F - populate form
		xfdftool -e/F <form.pdf> <input.xfdf/-> [output.pdf/-]
===
-awt/
-text/api
-text/log
-