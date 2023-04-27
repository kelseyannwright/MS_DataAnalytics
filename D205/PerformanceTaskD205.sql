--D205 Performance Task
--Kelseyann Wright, Western Governors University

--Research question: Do older customers purchase tech support services more often than younger customers? 


/* must run this before dropping services table if it exists due to connection with customer table
ALTER TABLE customer 
	DROP CONSTRAINT customer_services_id_fkey
*/

DROP TABLE IF EXISTS services --Drop table if it already exists

CREATE TABLE public.services --Create services table

(
	customer_id varchar(10),	
	InternetService	varchar(50),
	Phone varchar(3),	
	Multiple varchar(3),	
	OnlineSecurity varchar(3),	
	OnlineBackup varchar(3),	
	DeviceProtection varchar(3),	
	TechSupport varchar(3),
	PRIMARY KEY (customer_id)
)

--Import services.csv data using import/export dialog on PostgreSQL
--Import data runs the following command in psql terminal: \copy public.services (customer_id, internetservice, phone, multiple, onlinesecurity, onlinebackup, deviceprotection, techsupport) FROM '/Users/kelseyannwright/Desktop/WGU/D205/Data_Original/Services.csv' DELIMITER ',' CSV HEADER ; 


--Add relation to customer table for ERD
ALTER TABLE customer 
	ADD CONSTRAINT customer_services_id_fkey FOREIGN KEY (customer_id)
        REFERENCES public.services (customer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION

--Preview tables to check that they are loaded correctly 
SELECT * FROM services LIMIT 50
SELECT * FROM customer LIMIT 50

--verify that it is one row for each customer in services and customer table
SELECT count(customer_id) FROM services
SELECT count(customer_id) FROM customer

--Begin analysis to answer research question

DROP TABLE IF EXISTS age_techsupport --Drop temp table if it already exists

CREATE TEMPORARY TABLE age_techsupport AS  --Create temp table with subset of data to be used
SELECT 
	customer.customer_id, 
	CASE
		WHEN age <= 25 THEN '25 and Under'
		WHEN age BETWEEN 26 AND 35 THEN '26 to 35'
		WHEN age BETWEEN 36 AND 45 THEN '36 to 45'
		WHEN age BETWEEN 46 AND 55 THEN '46 to 55'
		WHEN age BETWEEN 56 AND 65 THEN '56 to 65'
		WHEN age > 65 THEN '66 and Over'
	END AS age_group,
	services.techsupport
FROM public.customer
JOIN public.services ON customer.customer_id = services.customer_id

--check temp table
SELECT * FROM age_techsupport 

---count number and percent of customers in each age group with tech support 
SELECT 
	age_techsupport.age_group,
	COUNT(CASE WHEN age_techsupport.techsupport = 'Yes' THEN 1 END) AS support_count,
	COUNT(age_techsupport) AS total_count,
	--calculate percentage - must convert integer to decimal for calculation (use ::decimal)
	(COUNT(CASE WHEN age_techsupport.techsupport = 'Yes' THEN 1 END)::decimal
	 	/COUNT(age_techsupport)::decimal)*100 AS percent_support
FROM age_techsupport
GROUP BY age_techsupport.age_group
ORDER BY age_techsupport.age_group
