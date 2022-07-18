# -*- coding: utf-8 -*-
'''
Utility module
@undocumented: __package__ logger __ch
'''

import logging
#import sys
from lxml import etree

# Log levels:
# DEBUG     error_log
# INFO
# WARNING
# ERROR
# CRITICAL

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
CH = logging.StreamHandler()  # default - stderr => /var/log/httpd/error_log
CH.setLevel(logging.DEBUG)
LOGGER.addHandler(CH)
LOG = LOGGER.debug     # logging function


def pprintxml_s(s_xml):
    '''
    Pretty print xml source.
    TODO: check s.startswith('<?xml')
    @param s_xml: source xml string
    @type s_xml: str
    @return: indented xml
    @rtype: str
    '''
    return etree.tostring(etree.fromstring(s_xml), pretty_print=True)


def pprintxml(e_xml):
    '''
    Pretty print xml source.
    @param e_xml: source xml
    @type e_xml: etree.Element
    @return: indented xml
    @rtype: str
    '''
    return etree.tostring(e_xml, pretty_print=True)
