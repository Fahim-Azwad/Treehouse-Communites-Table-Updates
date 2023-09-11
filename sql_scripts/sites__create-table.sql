CREATE TABLE public.sites (
	id int NOT NULL,
	bun varchar(36) NULL,
	company_id int NULL,
	property_id int NULL,
	resident_id int NULL,
	resident_group_id int NULL,
	region_name varchar(200) NULL,
	property_name varchar(200) NULL,
	site_name varchar(200) NULL,
	site_type varchar(36) NULL,
	site_status varchar(200) NULL,
	site_status_sos varchar(200) NULL,
	address_street_1 text NULL,
	address_street_2 text NULL,
	address_city varchar(200) NULL,
	address_state varchar(36) NULL,
	address_zip varchar(200) NULL,
	resident_name_first varchar(200) NULL,
	resident_name_last varchar(200) NULL,
	resident_email text NULL,
	resident_phone_home varchar(200) NULL,
	resident_phone_cell varchar(200) NULL,
	rent_home decimal(20, 3) NULL,
	rent_current decimal(20, 3) NULL,
	rent_market decimal(20, 3) NULL,
	rent_security_deposit decimal(20, 3) NULL,
	is_rental bool NULL,
	is_revenue_occupied bool NULL,
	is_vacant bool NULL,
	home_details json NULL,
	moveout_scheduled_date date NULL,
	date_created timestamp NOT NULL DEFAULT now(),
	date_modified timestamp NOT NULL DEFAULT now(),
	CONSTRAINT sites_pk PRIMARY KEY (id)
);
COMMENT ON TABLE public.sites IS 'Original data source names are in the comments';

-- Column comments

COMMENT ON COLUMN public.sites.id IS 'id';
COMMENT ON COLUMN public.sites.bun IS 'bun';
COMMENT ON COLUMN public.sites.company_id IS 'companyId';
COMMENT ON COLUMN public.sites.property_id IS 'propertyId';
COMMENT ON COLUMN public.sites.resident_id IS 'residentId';
COMMENT ON COLUMN public.sites.resident_group_id IS 'residentGroupId';
COMMENT ON COLUMN public.sites.region_name IS 'regionName';
COMMENT ON COLUMN public.sites.property_name IS 'propertyName';
COMMENT ON COLUMN public.sites.site_name IS 'name';
COMMENT ON COLUMN public.sites.site_type IS 'siteType';
COMMENT ON COLUMN public.sites.site_status IS 'status';
COMMENT ON COLUMN public.sites.site_status_sos IS 'sosStatus';
COMMENT ON COLUMN public.sites.address_street_1 IS 'address1';
COMMENT ON COLUMN public.sites.address_street_2 IS 'address2';
COMMENT ON COLUMN public.sites.address_city IS 'city';
COMMENT ON COLUMN public.sites.address_state IS 'state';
COMMENT ON COLUMN public.sites.address_zip IS 'postalCode';
COMMENT ON COLUMN public.sites.resident_name_first IS 'residentFirstName';
COMMENT ON COLUMN public.sites.resident_name_last IS 'residentLastName';
COMMENT ON COLUMN public.sites.resident_email IS 'residentEmail';
COMMENT ON COLUMN public.sites.resident_phone_home IS 'homePhone';
COMMENT ON COLUMN public.sites.resident_phone_cell IS 'cellPhone';
COMMENT ON COLUMN public.sites.rent_home IS 'homeRent';
COMMENT ON COLUMN public.sites.rent_current IS 'currentRent';
COMMENT ON COLUMN public.sites.rent_market IS 'marketRent';
COMMENT ON COLUMN public.sites.rent_security_deposit IS 'securityDeposit';
COMMENT ON COLUMN public.sites.is_rental IS 'isRental';
COMMENT ON COLUMN public.sites.is_revenue_occupied IS 'isRevenueOccupiedStatus';
COMMENT ON COLUMN public.sites.is_vacant IS 'isVacantStatus';
COMMENT ON COLUMN public.sites.home_details IS 'homeDetails';
COMMENT ON COLUMN public.sites.moveout_scheduled_date IS 'scheduledMoveoutDate';


create trigger update_modified before
update
	on
	public.sites for each row execute procedure update_modified();
