http://www.linux.org.ru/forum/development/2093852
http://xmlstar.sourceforge.net/doc/UG/ch05s01.html

Lib.rus.ec на 20131029 (http://torrent.rus.ec/viewtopic.php?p=60):
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

To test;
* repack zip into gz/bz2/lzma/xz
* unpack from ...

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
