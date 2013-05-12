-- Updating DB from 0.8 to 1.0
DROP TABLE `gw_jobrole`;
ALTER TABLE `sro2_orgsro` ADD COLUMN `aff` TINYINT  NOT NULL DEFAULT 0 AFTER `excludedate`;
ALTER TABLE `sro2_statement` ADD COLUMN `rejectprotocol_id` INTEGER  DEFAULT NULL AFTER `date`;

UPDATE `gw_contactaddrtype` SET name="Курьерский" WHERE id=4;
UPDATE `gw_addrshort` SET name="дер" WHERE id=29;
UPDATE `gw_addrshort` SET name="д" WHERE id=97;
UPDATE `gw_address` SET name=CONCAT(SUBSTRING(name,1,1),LOWER(SUBSTRING(name,2))), fullname=CONCAT(SUBSTRING(fullname,1,1),LOWER(SUBSTRING(fullname,2))) WHERE parent_id IS NULL;

ALTER TABLE `gw_address` ADD COLUMN `can_delete` TINYINT(1)  NOT NULL DEFAULT 0;


