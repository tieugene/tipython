#!/bin/sh
# prepare sources of lansite for packaging
NAME="lansite-sro"
VER=`cat ../ver` &&\
REL=`svn info | grep ^Revision | gawk '{print $2}'` &&\
TMPDIR=`mktemp -d` &&\
svn -q export .. $TMPDIR/$NAME-$VER &&\
pushd $TMPDIR/$NAME-$VER >/dev/null &&\
rm -rf _bin &&\
rm -f _contrib/data.* &&\
cd .. &&\
tar zcf $NAME-$VER-$REL.tar.gz $NAME-$VER &&\
popd >/dev/null &&\
mv $TMPDIR/$NAME-$VER-$REL.tar.gz . &&\
rm -rf $TMPDIR
