#!/bin/sh
LIB=itextpdf-5.2.1.jar
NAME=xfdftool
#NAME=Stage7
javac -cp "$LIB" MyPkg/$NAME.java &&\
java -cp ".:$LIB" MyPkg.$NAME $1 $2
