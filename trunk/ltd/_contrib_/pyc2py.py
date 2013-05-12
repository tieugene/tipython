""" Convert Python .pyc files (byte-code) to equivalent .py files.

    Usage: pyc2py.py <pyc filenames>

    Globbing is supported.  Note this script does not decompile the
    .pyc files !

    Copyright (c) 2006, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.

    License: eGenix.com Public License Agreement Version 1.0.0

"""#"
import marshal, struct, os, sys, glob, time

### Globals

# Version
__version__ = '1.0.0'

# Generate debug output ?
_debug = 0

# PYC Magic (taken from Python/import.c)
PYMAGIC = {
    20121: '1.5',
    50428: '1.6',
    50823: '2.0',
    60202: '2.1',
    60717: '2.2',
    62011: '2.3',
    62061: '2.4',
    62131: '2.5',
    }

# Template for the generated .py file
PY_TEMPLATE = """\
#!/usr/bin/env python
#
# Filename: %s
#
# Note: This file will only import in Python %s !
# Timestamp: %s
#
import marshal, imp
if imp.get_magic() != %r:
    raise ImportError('wrong Python version; need Python %s')
__code = marshal.loads(%r)
del marshal, imp
exec __code
del __code
"""

###

def read_pyc_file(pycfilename):

    f = open(pycfilename, 'rb')
    magic = f.read(4)
    timestamp = struct.unpack('<I', f.read(4))[0]
    code = f.read()
    # Ignore any remaining data in the file
    f.close()
    return magic, timestamp, code

def decode_magic(magic):

    value = struct.unpack('<H', magic[:2])[0]
    return PYMAGIC.get(value, '')

def write_py_file(pyfilename, magic, timestamp, code):

    f = open(pyfilename, 'wb')
    pyversion = decode_magic(magic)
    pycode = PY_TEMPLATE % (
        pyfilename,
        pyversion,
        time.ctime(timestamp),
        magic,
        pyversion,
        code)
    if _debug:
        print
        print '-' * 72
        print pycode
        print '-' * 72
        print
    f.write(pycode)
    f.close()

def convert(pycfilename):

    if pycfilename[-3:] not in ('pyc', 'pyo'):
        raise TypeError('%r is not a PYC file' % pycfilename)
    pyfilename = pycfilename[:-1]
    if os.path.exists(pyfilename):
        raise TypeError('%r already exists' % pyfilename)
    magic, timestamp, code = read_pyc_file(pycfilename)
    write_py_file(pyfilename, magic, timestamp, code)
    return pyfilename

def globargs(args=None):

    if args is None:
        args = sys.argv[1:]
    l = []
    for arg in args:
        if glob.has_magic(arg):
            # Glob pattern
            l.extend(glob.glob(arg))
        else:
            # Regular filename
            l.append(arg)
    return l

### Run as script

if __name__ == '__main__':
    for pycfilename in globargs():
        print '%s:' % pycfilename,
        try:
            pyfilename = convert(pycfilename)
        except (ValueError, TypeError), reason:
            print reason
        else:
            print pyfilename

