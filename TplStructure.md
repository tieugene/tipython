# Введение #

Описание подключаемого шаблона.

Note: smthng == любое имя


# Подробности #

Шаблон состоит из одного скрипта smthng.py - и одной или нескольких веб-страниц.

## Файлы ##

От корня приложения (обязательные - выделены жирным):

  * dox/tpl/**smthng.py** - бизнес-логика шаблона
  * templates:
    * form/smthng.xhtml - форма ввода
    * list/smthng.xhtml - список
    * print/**smthng.xhtml** - печатная форма
    * view/smthng.xhtml - форма просмотра

## Smthng.py ##

Имя:тип - комментарий

Обязательные выделены жирным.

  * **DATA**:SortedDict - описание данных
    * **u**:str - UUID шаблона - 32-символьный hex
    * **n**:str - Наименование - как оно будет выглядеть в списке шаблонов
    * c:str - Комментарий
    * **f**:dict - Описание данных
    * **t**:dict - Описание веб-страниц
      * **p**:str - Печатная форма
  * FORM:class
  * LIST:function
  * ANON:function
  * LIST:function
  * CREATE:function
  * READ:function
  * UPDATE:function
  * DELETE:function
  * PRINT:function
  * PRE\_LOAD/FORM/SAVE/PRINT:fucntion
  * POST