-- Database: churn

-- DROP DATABASE IF EXISTS churn;

CREATE DATABASE churn
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE churn
    IS 'D205 database';


CREATE TABLE public.contract
(
	contract_id integer NOT NULL,
	duration text COLLATE pg_catalog."default",
	CONSTRAINT contract_pkey PRIMARY KEY (contract_id)
)

CREATE TABLE public.job
(
	job_id integer NOT NULL,
	job_title text COLLATE pg_catalog."default",
	CONSTRAINT job_pkey PRIMARY KEY (job_id)
)

CREATE TABLE public.location
(
	location_id integer NOT NULL,
	zip integer,
	city text COLLATE pg_catalog."default",
	state text COLLATE pg_catalog."default",
	county text COLLATE pg_catalog."default",
	CONSTRAINT location_pkey PRIMARY KEY (location_id)
)

CREATE TABLE public.payment
(
	payment_id integer NOT NULL,
	payment_type text COLLATE pg_catalog."default",
	CONSTRAINT payment_pkey PRIMARY KEY (payment_id)
)


	
CREATE TABLE public.customer
(
	customer_id text COLLATE pg_catalog."default" NOT NULL,
	lat numeric,
	lng numeric,
	population integer,
	children integer,
	age integer,
	income numeric,
	marital text COLLATE pg_catalog."default",
	churn text COLLATE pg_catalog."default",
	gender text COLLATE pg_catalog."default",
	tenure numeric,
	monthly_charge numeric,
	bandwidth_gp_year numeric,
	outage_sec_week numeric,
	email integer,
	contacts integer,
	yearly_equip_faiure integer,
	techie text COLLATE pg_catalog."default",
	port_modem text COLLATE pg_catalog."default",
	tablet text COLLATE pg_catalog."default",
	job_id integer,
	payment_id integer,
	contract_id integer,
	location_id integer,
	CONSTRAINT customer_pkey PRIMARY KEY (customer_id),
	CONSTRAINT customer_contract_id_fkey FOREIGN KEY (contract_id)
		REFERENCES public.contract (contract_id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
		NOT VALID,
	CONSTRAINT customer_job_id_fkey FOREIGN KEY (job_id)
		REFERENCES public.job (job_id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
		NOT VALID,
	CONSTRAINT customer_location_id_fkey FOREIGN KEY (location_id)
		REFERENCES public.location (location_id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
		NOT VALID,
	CONSTRAINT customer_payment_id_fkey FOREIGN KEY (payment_id)
		REFERENCES public.payment (payment_id) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
		NOT VALID
)

