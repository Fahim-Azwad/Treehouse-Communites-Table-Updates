CREATE TABLE public.resident_new (
	id serial NOT NULL,
	fiscal_month int NULL,
	fiscal_year int NULL,
	bun varchar(32) NULL,
	property_id int NULL,
	site_id int NULL,
	resident_id int NULL,
	resident_group_id varchar(32) NULL,
	name_first varchar(200) NULL,
	name_last varchar(200) NULL,
	address_street_1 text NULL,
	address_street_2 text NULL,
	address_city varchar(200) NULL,
	address_state varchar(200) NULL,
	address_zip varchar(24) NULL,
	address_use_billing_char varchar(200) NULL,
	address_use_billing bool NULL,
	phone varchar(32) NULL,
	email text NULL,
	birthday_year int NULL,
	is_current bool NULL,
	is_current_1 varchar(1) NULL,
	is_current_2 varchar(1) NULL,
	site_address text NULL,
	site_type varchar(200) NULL,
	movein_reason text NULL,
	movein_date date NULL,
	movein_process_date date NULL,
	moveout_reason text NULL,
	moveout_date date NULL,
	moveout_process_date date NULL,
	moveout_schedule_date date NULL COLLATE "",
	moveout_schedule_reason text NULL,
	moveout_schedule_comment text NULL,
	moveout_schedule_removed varchar(24) NULL,
	moveout_schedule_sos varchar(200) NULL,
	moveout_sos_before varchar(200) NULL,
	moveout_sos_after varchar(200) NULL,
	sos varchar(200) NULL,
	rent_increase_last_date date NULL,
	rent_increase_next_anticipated_date date NULL,
	rent_increase_next_schedule_date date NULL,
	score_fico varchar(12) NULL,
	score_model int NULL,
	occ_count_additional int NULL,
	housing_cost_monthly_total decimal(20, 3) NULL,
	lease_agree_date date NULL,
	lease_expire_date date NULL,
	lease_description text NULL,
	date_created timestamp NOT NULL DEFAULT now(),
	date_modified timestamp NOT NULL DEFAULT now()
);
COMMENT ON TABLE public.resident_new IS 'Original column names are in the comments';

-- Column comments

COMMENT ON COLUMN public.resident_new.fiscal_month IS 'Fiscal Month';
COMMENT ON COLUMN public.resident_new.fiscal_year IS 'Fiscal Year';
COMMENT ON COLUMN public.resident_new.bun IS 'Bus Unit Number';
COMMENT ON COLUMN public.resident_new.property_id IS 'MA Prop Code';
COMMENT ON COLUMN public.resident_new.site_id IS 'Site ID';
COMMENT ON COLUMN public.resident_new.resident_id IS 'Resident ID';
COMMENT ON COLUMN public.resident_new.resident_group_id IS 'Resident Group ID';
COMMENT ON COLUMN public.resident_new.name_first IS 'First Name';
COMMENT ON COLUMN public.resident_new.name_last IS 'Last Name';
COMMENT ON COLUMN public.resident_new.address_street_1 IS 'Address1';
COMMENT ON COLUMN public.resident_new.address_street_2 IS 'Address2';
COMMENT ON COLUMN public.resident_new.address_city IS 'City';
COMMENT ON COLUMN public.resident_new.address_state IS 'State';
COMMENT ON COLUMN public.resident_new.address_zip IS 'Zip';
COMMENT ON COLUMN public.resident_new.address_use_billing_char IS 'Use Billing Address';
COMMENT ON COLUMN public.resident_new.phone IS 'Phone';
COMMENT ON COLUMN public.resident_new.email IS 'EMail';
COMMENT ON COLUMN public.resident_new.birthday_year IS 'Year Of Birth';
COMMENT ON COLUMN public.resident_new.is_current_1 IS 'Current Or Former';
COMMENT ON COLUMN public.resident_new.is_current_2 IS 'Current Resident';
COMMENT ON COLUMN public.resident_new.site_address IS 'Site Address';
COMMENT ON COLUMN public.resident_new.site_type IS 'Site Type';
COMMENT ON COLUMN public.resident_new.movein_reason IS 'MI Reason';
COMMENT ON COLUMN public.resident_new.movein_date IS 'Move In Date';
COMMENT ON COLUMN public.resident_new.movein_process_date IS 'Move In Process Date';
COMMENT ON COLUMN public.resident_new.moveout_reason IS 'MO Reason';
COMMENT ON COLUMN public.resident_new.moveout_date IS 'Move Out Date';
COMMENT ON COLUMN public.resident_new.moveout_process_date IS 'Move Out Process Date';
COMMENT ON COLUMN public.resident_new.moveout_schedule_date IS 'Scheduled Move Out Date';
COMMENT ON COLUMN public.resident_new.moveout_schedule_reason IS 'Scheduled Move Out Reason';
COMMENT ON COLUMN public.resident_new.moveout_schedule_comment IS 'Scheduled Move Out Comments';
COMMENT ON COLUMN public.resident_new.moveout_schedule_removed IS 'Scheduled Move Out Removed';
COMMENT ON COLUMN public.resident_new.moveout_schedule_sos IS 'Scheduled Move Out SOS';
COMMENT ON COLUMN public.resident_new.moveout_sos_before IS 'SOS Before Moveout';
COMMENT ON COLUMN public.resident_new.moveout_sos_after IS 'SOS After Moveout';
COMMENT ON COLUMN public.resident_new.sos IS 'SOS';
COMMENT ON COLUMN public.resident_new.rent_increase_last_date IS 'Last Implemented Scheduled Rent Increase Date';
COMMENT ON COLUMN public.resident_new.rent_increase_next_anticipated_date IS 'Next Anticipated Rent Increase Date';
COMMENT ON COLUMN public.resident_new.rent_increase_next_schedule_date IS 'Next Scheduled Rent Increase Date';
COMMENT ON COLUMN public.resident_new.score_fico IS 'FICO Score';
COMMENT ON COLUMN public.resident_new.score_model IS 'Model Score';
COMMENT ON COLUMN public.resident_new.occ_count_additional IS 'Addtl Occ Count';
COMMENT ON COLUMN public.resident_new.housing_cost_monthly_total IS 'Total Monthly Housing Cost';
COMMENT ON COLUMN public.resident_new.lease_agree_date IS 'Lease Agreement Date';
COMMENT ON COLUMN public.resident_new.lease_expire_date IS 'Lease Expiration Date';
COMMENT ON COLUMN public.resident_new.lease_description IS 'Lease Description';

create trigger update_modified before
update
	on
	public.resident_new for each row execute procedure update_modified();
