http://www.linux.org.ru/forum/development/2093852
http://xmlstar.sourceforge.net/doc/UG/ch05s01.html
http://www.fictionbook.org/index.php/%D0%AD%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D1%8B_%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%B0_FictionBook

http://traumlibrary.net/

Timer (1GB):
* unzip all > /dev/null: 31"
* unzip all > tmp/: 70"
* unzip each > null: 61"
* unzip each > tmp/: 97"
* unzip all > null: 55'18"
* 0_split-3 fb2-203897-204340.zip (95MB, 293 files): 75"
* 0_extract-3 fb2-203897-204340.zip (95MB, 293 files): 23" (1st - 18'27")
* 0_extract-3 fb2-203897-204340.zip (95MB, 293 files): 19" (1st - 12'12")

01-01:	0732"
02-10:	0392"
11-20:	2349"
21-35:	3276" (fb2-193823-199572.zip..fb2-292000-299999.zip)
36-65:	127m53.538s (fb2-193823-199572.zip..fb2-292000-299999.zip)

expanded: 270133 (24 oops - это дубли)

Чюдеса:
--w-rw-rw- 1 eugene users 3375356 янв 20  2009 137241.fb2
--w-rw-rw- 1 eugene users 4557369 янв 20  2009 137273.fb2
--w-rw-rw- 1 eugene users 1025894 янв 23  2009 137532.fb2
--w-rw-rw- 1 eugene users 2326463 янв 23  2009 137579.fb2

Cover:
	* in title-info, src-title-info - 0..1
	* image - 1+

Lib.rus.ec на 20131029 (http://torrent.rus.ec/viewtopic.php?p=60):
* 97GB
* 65 архива
* 270157 файлов (till 453...) - 270133 уникальных (24 - дубли)

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

= Try =
* перепаковать (unzip => XXX/000yyy.gz/bz2/xz/7z) - еще 100 гигов)
* time:
** unzip all (3.5"):
	time unzip -q -c src/fb2-203897-204340.zip >/dev/null
** unzip each (5.5"):
	z="src/fb2-203897-204340.zip"; time for i in `zipinfo -1 $z`; do unzip -q -c $z $i > /dev/null; done
** unzip each into tmp (5.5", 53.. fps (src/fb2-203897-204340.zip..):
	time (z="src/fb2-203897-204340.zip"; t=`mktemp`; for i in `zipinfo -1 $z`; do unzip -q -c $z $i > $t; done; rm -f $t)
* => - bash w/ inram tmpfile:
** unzip to tmpfile
** cut header (if possible...0
** enca -r <file> => USC-2 | iconv ... | sed ... | sed (utf-16/utf-8))
** parse header on images > stdout
** cut <binaries (sed) | parse_bin
* unpack (305226.fp refubished):
** unzip = 0.05
? ну или не прошедшие xml (2584) - скипать и ждать патчей (bsdiff, libxdiff, vbindiff, xdelta)
* compare unpack | epack w/ unpack

= Ideas =
* CRC64 as fo zip as for files inside (CRC-64-ISO, CRC-64-ECMA)
* TheLib - all of fb2s (id == CRC64/MD5)

= TODO =
FictionBook
- desciption (1)
  - title-info (1)
    - author (+)
      - first-name - str
      - middle-name - st
      - last-name - str
      - nickname
      - ?id
    - genre (+) - str
    - book-title (1) - str
    - annotation (?)
      - p
      - poem
      - cite
      - subtitle
      - empty-line
      - ?table
    - coverpage (?)
      - image (+)
        - => binary
    - lang - str
    - sequence (*) - str, int

DB:
= Main =
= Refs =
* lang:
    * name
    * desc[ru]
    * desk[en]
    * Aliases[]
* genre:
    * name
    * desk[ru]
    * desk[en]
    * Aliases
* Author:
    * lastname[ru, en]
    * firstname[ru, en]
    * midname[ru, en]
    * nickname[ru, en]
    * IDs (lib.rus.ec.id, flibusta id, etc)

= INP format =
http://forum.home-lib.net/index.php?/forum/17-inpx/
http://forum.home-lib.net/index.php?/topic/329-%D0%BA%D0%B0%D0%BA-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-inpx-%D1%84%D0%B0%D0%B9%D0%BB-librusec-online/
AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;
* кодировка - UTF-8
* строка заканчивается ^M
* каждое поле разделяется ^D:
-- Фамилия,[Имя],[Отчество]: x *
-- category:
-- title
--