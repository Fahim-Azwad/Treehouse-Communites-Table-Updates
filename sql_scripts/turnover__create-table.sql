CREATE TABLE public.turnover_new (
	pid serial4 NOT NULL,
	turnover_id int4 NULL,
	group_id int4 NULL,
	site_id int4 NULL,  
	property_id int4 NULL,
	bun int4 NULL,
	site_name varchar(20) NULL,
	turnover_type varchar(20) NULL,
	is_movein bool NULL,
	name_first varchar(50) NULL,
	name_last varchar(50) NULL,
	movein_date timestamp NULL,
	movein_processed_date timestamp NULL,
	moveout_date timestamp NULL,
	moveout_processed_date timestamp NULL,
	sos_new varchar(50) NULL,
	sos_previous varchar(50) NULL,
	reason_description text NULL,
	reason_resident_moveout text NULL,
	date_created timestamp NOT NULL DEFAULT now(),
	date_modified timestamp NOT NULL DEFAULT now(),
	CONSTRAINT turnover_new_pkey PRIMARY KEY (pid)
);


create trigger items_null_pid_is_default before
insert
    on
    public.turnover_new for each row execute procedure items_null_pid_is_default();

create trigger update_modified before
update
    on
    public.turnover_new for each row execute procedure update_modified();
