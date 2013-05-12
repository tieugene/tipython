#!/bin/sh
MGR="../manage.py"

echo "-------------------------------------- 1. Svn update -------------------------------------------"
svn update ..

echo "-------------------------------------- 1. Change permissions -----------------------------------"
chmod -R a+rw ..
chmod a+rwx patch.sh
chmod a+rwx ver.py
chmod a+rwx ../manage.py

echo "-------------------------------------- 2. Database synchronization -----------------------------"
echo "no" | $MGR syncdb

echo "-------------------------------------- 3. Database update --------------------------------------"
mysql -ulansite -plansite lansite < patch.sql

echo "-------------------------------------- 3. Version update ---------------------------------------"
echo -n "Enter the new version: "
read version
./ver.py -c $version

echo "-------------------------------------- 4. Apache restart ---------------------------------------"
/etc/init.d/httpd restart

echo "-------------------------------------- Lansite's been updated. ---------------------------------"
