#!/usr/bin/env python
# Change project version

__author__ = 'Averrin'
__version__ = '0.2'


import re
import optparse

def main():
    p=optparse.OptionParser(description="Change project version", prog='lansite_version', version='0.1', usage="%prog [command]")
    p.add_option('--custom-ver','-c',action='store',help='custom version', type="string", dest="newver",default='')
    p.add_option('--custom-postfix','-p',action='store',help='custom postfix', type="string", dest="postfix",default='')
    options, arguments = p.parse_args()
    try:
        f=open('../ver','r')
        VERSION=f.read()
        f.close()
        print 'Old ver:'

        ver = re.findall('(\d)\.(\d)\.(\d)',VERSION)[0]
        try:
            pf = re.findall('\d\.\d\.\d ([^ ]*)',VERSION)[0]
        except:
            pf=''
        oldver='.'.join(ver[0:3])+' '+pf
        print VERSION
        if not options.newver:
            build=int(ver[2])+1
            newver='%s.%s.%d' % (ver[0],ver[1],build)
        else:
            newver=options.newver
        if options.postfix:
            newver+=' '+options.postfix
        else:
            newver+=' '+pf
        VERSION=newver
        print 'New ver'
        print VERSION
        f=open('../ver','w')
        f.write(VERSION)
        f.close()

    except Exception,e:
        print e

if __name__ == '__main__':
    main()
