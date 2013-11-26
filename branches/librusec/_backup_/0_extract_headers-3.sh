#!/bin/sh
# tool to extract headers from ziped fb2s (ver.3 - xml 1st).
# Usage: extract_headers.sh <librusec dir> <output dir>
SRCDIR="src"
DSTDIR="dst"
TMPDIR="tmp"
ERRDIR="err"

CUDIR=""
TMP=`mktemp -q`
TMP1=`mktemp -q`

for j in `cat librusec.lst`; do
	unzip -q -d $TMPDIR $SRCDIR/$j
	for i in `ls $TMPDIR`; do
		# 0. prepare
		#echo $i
		FILENAME=`basename $i .fb2`
		FULLNAME=`printf '%06d' $FILENAME`
		OUTDIR=$DSTDIR/`echo $FULLNAME | cut -c1-3`
		if [[ $CURDIR != $OUTDIR ]]; then
			if [ ! -d "$OUTDIR" ]; then mkdir $OUTDIR; fi
			CURDIR=$OUTDIR
		fi
		SRCFILE="$TMPDIR/$i"
		DSTFILE="$OUTDIR/$FULLNAME.xml"

		XMLLINT_INDENT=" " xmllint --format --encode utf-8 --noblanks --nonet --recover --output $TMP $SRCFILE 2>/dev/null
		if [ $? -eq 0 ]; then
			# 1. Plan A - valid xml
			sed -n -e '/<?xml/,/<\/description>/p' $TMP > $TMP1
			if [ -s $TMP1 ]; then
				(cat $TMP1; echo "</FictionBook>") > $DSTFILE
				#echo "$i Plan A ok"
			else
				echo "$i Plan A: header not found" >&2
				mv -f $TMP $ERRDIR/$FULLNAME.fb2
			fi
			rm -f $SRCFILE
		else
			# 2. Plan B - invalid xml
			sed -n -e '/<?xml/,/<\/description>/p' $SRCFILE > $TMP
			if [ -s $TMP ]; then
				(cat $TMP; echo "</FictionBook>") | XMLLINT_INDENT=" " xmllint --format --encode utf-8 --noblanks --nonet --recover --output $DSTFILE -
				if [ $? -ne 0 ]; then
					echo "$i Plan B: invalid xml" >&2
					(cat $TMP; echo "</FictionBook>") > $ERRDIR/$FULLNAME.xml
				#else
				#	echo "$i Plan B ok"
				fi
				rm -f $SRCFILE
			else
				echo "$i Plan B: header not found" >&2
				mv -f $SRCFILE $ERRDIR/$FULLNAME.fb2
			fi
		fi
	done
done
rm -f $TMP $TMP1
