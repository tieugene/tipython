#!/bin/sh
# Скрипт ДЛЯ СПРАВКИ!
MGR="./manage.py"
DBNAME=`python -c "import settings; print settings.DATABASE_NAME;"`
DBUSER=`python -c "import settings; print settings.DATABASE_USER;"`
DBPASS=`python -c "import settings; print settings.DATABASE_PASSWORD;"`

FILES="apps/gw/contact/models.py apps/sro2/forms.py apps/sro2/models.py apps/sro2/shared.py apps/sro2/urls.py apps/sro2/views.py"

## 0. svn update
#echo "0. svn update"
#svn update

## 1. старая схема
echo "1. Restore old scheme"
for i in $FILES; do sed -i -e 's/###(1/"""(1/;s/###1)/1)"""/;s/"""(2/###(2/;s/2)"""/###2)/;' $i; done

## 2. Прибить базу:
echo "2. Kill DB"
(echo "BEGIN;" && (echo "SHOW TABLES;" | $MGR dbshell | grep -v Tables | while read i; do echo "DROP TABLE $i;"; done) && echo "COMMIT;") | $MGR dbshell

## 3. Создать схему:
echo "3. Create old scheme"
echo "no" | $MGR syncdb > 3.log

## 4. Внести gw: 11"15' @ host050
echo "4. Restore gw data"
(echo "BEGIN;" && _bin/tunedump2.py _data/gw_1.sql.gz 2>4.err && echo "COMMIT;") | $MGR dbshell

## 5. Внести свежее sro:
echo "5. Restore fresh sro data"
(echo "BEGIN;" && _bin/tunedump2.py `./getlastdump.sh` 2>5.err && echo "COMMIT;") | $MGR dbshell

## 6. перенос данных с помощью view "models2gw"
#echo "6. Move objects to gw"
#ip=`/sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
#python -c "import urllib2; from settings import LOGIN_REDIRECT_URL; page = urllib2.urlopen('http://' + '$ip' + LOGIN_REDIRECT_URL + 'sro2/models2gw/'); result = page.read(); print result;"

## 7. Вернуть всё взад
#echo "7. Restore new models"
#for i in $FILES; do sed -i -e 's/###(2/"""(2/;s/###2)/2)"""/;s/"""(1/###(1/;s/1)"""/###1)/;' $i; done

## 8. и подлампичить
#echo "8. Tuning"
#SQL="ALTER TABLE gw_org DROP COLUMN old_user_id; ALTER TABLE gw_person DROP COLUMN old_user_id;"
## ALTER TABLE sro2_orgsro DROP INDEX org_id; ALTER TABLE sro2_personskill DROP COLUMN courseno, DROP COLUMN coursedate, DROP COLUMN coursename, DROP COLUMN courseschool;"
#echo "BEGIN; $SQL COMMIT;" | $MGR dbshell

echo "x. That's all, folks"
