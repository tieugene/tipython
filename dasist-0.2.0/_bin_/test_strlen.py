#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Test string lengths.
Models: grep ^\ \"model data.json | sort | uniq
'''

import json
import pprint

TO_TEST = {
    'core.file':        {
        'name':     0,
        'mime':     0,
    },
    'core.org':         {
        'name':     0,
        'fullname': 0,
    },
    'invarch.invarch':        {
        'place':    0,
        'subject':  0,
        'depart':   0,
        'payer':    0,
        'supplier': 0,
        'no':       0,
    },
    'invarch.event':       {
        'approve':  0,
        'comment':  0,
    },
    'invoice.state':      {
        'name':     0,
        'color':    0,
    },
    'invoice.role':       {
        'name':     0,
    },
    'invoice.approver':   {
        'jobtit':   0,
    },
    'invoice.place':      {
        'name':     0,
    },
    'invoice.subject':    {
        'name':     0,
    },
    'invoice.department': {
        'name':     0,
    },
    'invoice.payer':      {
        'name':     0,
    },
    'invoice.bill':       {
        'supplier': 0,
        'billno':   0,
    },
    'invoice.event':      {
        'comment':  0,
    },
}


def result():
    pass


def main(infile):
    data = json.load(open(infile))
    for rec in data:    # dict
        totest = TO_TEST.get(rec['model'])    # TO_TEST record
        if totest:
            for k, v in rec['fields'].iteritems():
                if (k in totest) and v:
                    # print rec['model'], k, v
                    totest[k] = max(totest[k], len(v))
                    if len(v) > 255:
                        print rec['model'], rec['pk']
    pprint.pprint(TO_TEST)


if (__name__ == '__main__'):
    main('data.json')
