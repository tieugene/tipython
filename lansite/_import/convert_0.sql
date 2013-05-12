-- convert from production to trunk
BEGIN;
-- remove unneed
-- 1. models
DELETE FROM data WHERE model IN (
	'gw_gwuser',
	'gw_speciality',
	'gw_skill',
	'gw_personskill',
	'gw_course',
	'gw_okato',
	'gw_okopf',
	'gw_okved',
	'gw_role',
	'gw_vcal'
);
-- 2. permissions
DELETE FROM data WHERE model='auth_permission' AND record IN (
	SELECT record FROM data WHERE model='auth_permission' AND field='content_type_id' AND value IN (
		SELECT d0.record FROM data AS d0 JOIN (
			SELECT model, record, value FROM data WHERE model='django_content_type' AND field='app_label'
		) AS d1 ON d0.model=d1.model AND d0.record=d1.record
		WHERE d0.model='django_content_type' AND d0.field='model' AND d1.value='gw' AND d0.value IN (
			'gwuser',
			'speciality',
			'skill',
			'personskill',
			'course',
			'okato',
			'okopf',
			'okved',
			'role',
			'vcal'
		)
	)
);
-- 3. contenttypes
DELETE FROM data WHERE model='django_content_type' AND record IN (
	SELECT d0.record FROM data AS d0 JOIN (
		SELECT model, record, value FROM data WHERE model='django_content_type' AND field='app_label'
	) AS d1 ON d0.model=d1.model AND d0.record=d1.record
	WHERE d0.model='django_content_type' AND d0.field='model' AND d1.value='gw' AND d0.value IN (
		'gwuser',
		'speciality',
		'skill',
		'personskill',
		'course',
		'okato',
		'okopf',
		'okved',
		'role',
		'vcal'
	)
);
-- UPDATE data SET value='jobrole' WHERE model='django_content_type' AND field='model' AND value='role';
-- 4. misc
DELETE FROM data WHERE model='gw_person' AND field='user';
DELETE FROM data WHERE model='gw_org' AND field IN ('foreign', 'laddress', 'raddress');
UPDATE data SET value=value*1000000 WHERE model='gw_org' AND field='okato';
-- UPDATE data SET model='gw_jobrole' WHERE model='gw_role';
DELETE FROM data WHERE model='gw_orgstuff' AND field IN ('leader', 'permanent', 'startdate', 'enddate');
COMMIT;
