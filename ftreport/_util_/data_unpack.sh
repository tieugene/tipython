#!/bin/sh
for i in `ls _data_`; do YMD=`basename $i .tar` && mkdir $YMD && tar xf _data_/$i -C $YMD; done
