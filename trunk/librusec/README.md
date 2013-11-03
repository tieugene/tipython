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

= To test =
* time unzip -q -c ... > /dev/null
* => - bash w/ inram tmpfile:
** unzip to tmpfile
** cut header (if possible...0
** enca -r <file> => USC-2 | iconv ... | sed ... | sed (utf-16/utf-8))
** parse header on images > stdout
** cut <binaries (sed) | parse_bin

= Ideas =
* CRC64 as fo zip as for files inside (CRC-64-ISO, CRC-64-ECMA)

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
