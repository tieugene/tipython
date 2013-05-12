#!/bin/sh
# converts html to xhtml
tidy -w 0 -utf8 -asxml $1 > `basename $1 .html`.xhtml
