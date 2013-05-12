#!/bin/sh
# make tarball for rpm
VER=0.0.1
BACK=`pwd`
DEST=`mktemp -d` && \
mkdir $DEST/xfdftool-0.0.1 && \
cp -r {xfdftool,Manifest.txt} $DEST/xfdftool-0.0.1 && \
mkdir $DEST/xfdftool-0.0.1/MyPkg && \
cp MyPkg/xfdftool.java $DEST/xfdftool-0.0.1/MyPkg && \
pushd $DEST>/dev/null && \
tar jcf $BACK/xfdftool-0.0.1.tar.bz2 xfdftool-0.0.1 && \
popd>/dev/null && \
rm -rf $DEST