#!/bin/sh
# Dump data to initial data archive
TABLES="ref_kladr ref_kladrokato ref_kladrshort ref_kladrstatetype ref_okato ref_okopf ref_oksm gw_address gw_addrshort gw_addrkladr gw_okato gw_okopf gw_okved sro2_reason sro2_srotype sro2_stagever sro2_stage"

pushd .. >/dev/null
MGR="./manage.py"
DBNAME=`python -c "import settings; print settings.DATABASE_NAME;"`
DBUSER=`python -c "import settings; print settings.DATABASE_USER;"`
DBPASS=`python -c "import settings; print settings.DATABASE_PASSWORD;"`

TEMP=`mktemp -d`
ARCH=`pwd`/data.7z
pushd $TEMP >/dev/null
for t in $TABLES
do
	mysqldump --user=$DBUSER --password=$DBPASS -c --compact -e --skip-opt -t $DBNAME $t > $t.sql
	7za a $ARCH $t.sql
	rm -f $t.sql
done
echo "INSERT INTO gw_object (id, polymorphic_ctype_id) SELECT object_ptr_id, (SELECT id FROM django_content_type WHERE app_label='gw' AND model='address') FROM gw_address;" > gw_object.sql
7za a $ARCH gw_object.sql
popd >/dev/null
popd >/dev/null
