-- PostSqlite: optimize data for import (30"); Don't forget VACUUM
BEGIN;
-- 1. drop Object (they are empty)
DELETE FROM data WHERE model='gw_object';
-- 2. File => ImageFile
UPDATE data SET model='gw_imagefile' WHERE model='gw_file' AND record IN (SELECT record FROM data WHERE model='gw_imagefile');
-- 3. Task => vCal
UPDATE data SET model='gw_vtodo' WHERE model='gw_task' AND record IN (SELECT record FROM data WHERE model='gw_vcal');
-- 4. vCal => vEvent
UPDATE data SET model='gw_vevent' WHERE model='gw_vcal' AND record IN (SELECT record FROM data WHERE model='gw_vevent');
-- 5. vCal => vToDo
UPDATE data SET model='gw_vtodo' WHERE model='gw_vcal' AND record IN (SELECT record FROM data WHERE model='gw_vtodo');
-- 6. That's all
COMMIT;
