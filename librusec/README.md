Lib.rus.ec на 20131029:
* 95GB
* 64 архива
* 266100 файлов
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

dos2unix *.fb2
xmlindent -i0 *.fb2
