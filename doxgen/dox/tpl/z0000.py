# -*- coding: utf-8 -*-
'''
Пример
'''

from django.utils.datastructures import SortedDict
import sys
from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')


DATA = {
	K_T_UUID:	'58ACC2A6E62C4574B3BE91475D5ACB98',
	K_T_NAME:	'Пример',
	K_T_COMMENTS:	'Пример шаблона',
	K_T_FIELD:	SortedDict([]),
	K_T_T:	{
		K_T_T_PRINT:	'print/z0000.html',
	}
}
