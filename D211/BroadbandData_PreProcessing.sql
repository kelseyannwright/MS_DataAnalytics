UPDATE broadband
	SET county_name = REPLACE (county_name, ' County', '');

UPDATE broadband
	SET county_name = REPLACE (county_name, ' City and Borough', '');

UPDATE broadband
	SET county_name = REPLACE (county_name, ' Borough', '');
	
UPDATE broadband
	SET county_name = REPLACE (county_name, ' Census Area', '');
	
UPDATE broadband
	SET county_name = REPLACE (county_name, ' Municipality', '');

UPDATE broadband
	SET county_name = REPLACE (county_name, ' Parish', '');

UPDATE broadband
	SET county_name = REPLACE (county_name, ' city', '') 
	
SELECT * FROM broadband
