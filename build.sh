#!/bin/sh
# build resulting jar
ant && \
unzip -q itextpdf-5.3.0.jar && \
rm -rf META-INF && \
zip -m -r -q xfdftool.jar com
