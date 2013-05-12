-- PostSqlite: optimize data for import (30"); Don't forget VACUUM
BEGIN;
-- 1. drop Object (they are empty)
DELETE FROM data WHERE model='gw_object';
-- 2. File => ImageFile
UPDATE data SET model='gw_imagefile' WHERE model='gw_file' AND record IN (SELECT record FROM data WHERE model='gw_imagefile');
-- 3. Task => vEvent
UPDATE data SET model='gw_vevent' WHERE model='gw_task' AND record IN (SELECT DISTINCT record FROM data WHERE model='gw_vevent');
-- 4. Task => vToDo
UPDATE data SET model='gw_vtodo' WHERE model='gw_task' AND record IN (SELECT DISTINCT record FROM data WHERE model='gw_vtodo');
-- 5. Contact => Person
UPDATE data SET model='gw_person' WHERE model='gw_contact' AND record IN (SELECT DISTINCT record FROM data WHERE model='gw_person');
-- 6. Contact => Org
UPDATE data SET model='gw_org' WHERE model='gw_contact' AND record IN (SELECT DISTINCT record FROM data WHERE model='gw_org');
-- X. That's all
COMMIT;
