Lib.rus.ec на 20131029:
* 95GB
* 64 архива
* 266100 файлов (till 453299)
(zipinfo -t $i | gawk '{pint $1}')

Todo:
* extract header only (_contrib_/FB2_DB.svg) - FictionBook/(description,binary)
- find </description>
- отрезать после него
- выгрузить
- понаходить все binary
- выгрузить
- закрыть </FictionBook>
- ну или вырезать всё кроме body
- и/или сначала xmlindent

cat *.fb2 | dos2unix | xmlindent -i0 | extract_header.py > ...
folders: 453 folders with up to 999 files

Try: xmlwf

----
Еще вариант xract_header: cp stdin > stdout: (body может быть несколько
* от начала до </description> и от <binary - и до конца
* или вырезать <stylesheet ..</stylesheet> и <body..</body>
