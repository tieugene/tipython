#!/bin/sh
javac -cp "/usr/share/java/itextpdf.jar" part2/chapter06/FormInformation.java part2/chapter08/ReaderEnabledForm.java && \
java -cp ".:/usr/share/java/itextpdf.jar" part2.chapter06.FormInformation
