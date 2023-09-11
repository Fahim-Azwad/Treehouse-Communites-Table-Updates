
CREATE TABLE public.property_new (
	property_id int4 NOT NULL,
	company_id int4 NULL,
	region_id int4 NULL,
	portfolio_id int4 NULL,
	bun varchar NULL,
	division varchar(20) NULL,
	region_name varchar(200) NULL,
	portfolio_name varchar(200) NULL,
	name text NULL,
	phone text NULL,
	email text NULL,
	address_street text NULL,
	address_city varchar(20) NULL,
	address_state varchar(3) NULL,
	address_county varchar(20) NULL,
	address_zip int4 NULL,
	fiscal_month int4 NULL,
	fiscal_year int4 NULL,
	date_created timestamp NOT NULL DEFAULT now(),
	date_modified timestamp NOT NULL DEFAULT now(),
	CONSTRAINT property_pkey PRIMARY KEY (property_id)
);

-- Table Triggers

create trigger update_modified before
update
	on
	public.property_new for each row execute procedure update_modified();
