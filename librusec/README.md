Lib.rus.ec на 20131029:
* 95GB
* 64 архива
* 266100 файлов (till 453299)

Stages:
+0. split fb2 into dumb headers and cover images (10 zips/6h)
+1. chkeck, format and recode them (XMLLINT_INDENT=" " xmllint --format --encode UTF-8 --noblanks --nonet --output)
 2. stat
 3. fill db
 4. Web UI

= TODO =
== 0 ==
* split_fb2.py:
** parse in try-except
* split_fb2.sh:
** remove dos2unix
** quiet
** err handling
** xmllint?
** testing zip (bad header, bad binary)
* make AIO split... (for zip, file and stdin) (because *.py loading and parsing everywhen):
** exact 3 args:
*** in (folder/zip/fb2/-)
*** hdr out (dir/-)
*** img dir
== 1 ==
* ?simplified xml scheme
== 2 ==
in descrription/title-info
* authors (uniq, count, id)
* tags inside annotation (count)
* genres (count, count per file)
* lang

= Ideas =
* CRC64 as fo zip as for files inside (CRC-64-ISO, CRC-64-ECMA)
