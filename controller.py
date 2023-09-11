""" All posgres insert roiutines are in the same file (this file).
This is done so update order can be enforced (ex: update property before turnover)

Running this file will update everything- but that behavior can be overridden by using command line flags.

EXAMPLE CMD INPUTS
	Update everything
		>> python postgres-insert-all.py

	Only update the property table
		>> python postgres-insert-all.py --property

	Only update the property and turnover table
		>> python postgres-insert-all.py --property --turnover

	See a complete list of the available flags
		>> python postgres-insert-all.py --help
"""

import sys
import urllib
import argparse
import datetime
import dateutil.relativedelta

sys.path.append("../PyUtilities")
import common
import logger
import database


@common.tryExcept
@logger.logger_timer("property")
def doProperty(print_time=False):
	def modifyData_extractJson(data):
		""" Extracts the JSON data to it's own columns. """

		for row in data:
			for key in ["region", "portfolio"]:
				catalogue = row[key]

				row[f"{key}_id"] = catalogue["id"]
				row[f"{key}_name"] = catalogue["name"]

				del row[key]
		return data

	def modifyData_treehouse(data):
		""" Updates the treehouse IDs so they are unique. """

		for row in data:
			row["property_id"] = f"{row['property_id']}165"
			row["region_id"] = f"{row['region_id']}165"
			row["portfolio_id"] = f"{row['portfolio_id']}165"
		return data

	# Send vineyards data
	database.posgres_insert(
		data=database.ma_getData(
			url="https://n6.manageamerica.com/api/property/?companyId=233",
			login_user="VinApi",
			login_password="9@%sZqRxDeZ@38s",
			modifyData=modifyData_extractJson,
			alias={
				"id": "property_id",
				"companyId": "company_id",
				"address": "address_street",
				"city": "address_city",
				"state": "address_state",
				"county": "address_county",
				"zip": "address_zip",
				"fiscalMonth": "fiscal_month",
				"fiscalYear": "fiscal_year",
			},
		),
		table="property",
		method="upsert",
	)

	## Send treehouse data
	database.posgres_insert(
		data=database.ma_getData(
			url="https://n9.manageamerica.com/api/property/?companyId=165",
			login_user="jhult1",
			login_password="Thouse33!",
			modifyData=[modifyData_extractJson, modifyData_treehouse],
			alias={
				"id": "property_id",
				"companyId": "company_id",
				"address": "address_street",
				"city": "address_city",
				"state": "address_state",
				"county": "address_county",
				"zip": "address_zip",
				"fiscalMonth": "fiscal_month",
				"fiscalYear": "fiscal_year",
			},
		),
		table="property",
		method="upsert",
	)

	if (print_time):
		logger.logger_timer_print("property")



@common.tryExcept
@logger.logger_timer("occupancy")
def doOccupancy(print_time=False):
	database.posgres_insert(
		data=database.ma_getData(
			url="https://n6.manageamerica.com/api/property/occupancy/?pool=mh",
			login_user="VinApi",
			login_password="9@%sZqRxDeZ@38s",
			alias={
				"numSites": "site_count",
			},
		),
		table="occupancy",
		method="upsert",
		backup="dropbox",
		typeCatalogue={
			"occupancy": "json",
		},
	)

	if (print_time):
		logger.logger_timer_print("occupancy")



@common.tryExcept
@logger.logger_timer("sites")
def doSites(print_time=False):
	properties = database.posgres_raw(query_sql="SELECT property_id, company_id FROM property", as_dict=False)

	date_from = datetime.datetime.now()
	date_filter = f"year={date_from.year}&month={date_from.month}"

	database.posgres_insert(
		data=database.ma_getData(
			url=(f"https://n6.manageamerica.com/api/v1/sites/?companyId={companyId}&propertyId={propertyId}&{date_filter}" for (propertyId, companyId) in properties),
			login_user="VinApi",
			login_password="9@%sZqRxDeZ@38s",
			alias={
				"companyId": "company_id",
				"propertyId": "property_id",
				"residentId": "resident_id",
				"residentGroupId": "resident_group_id",
				"regionName": "region_name",
				"propertyName": "property_name",
				"name": "site_name",
				"siteType": "site_type",
				"status": "site_status",
				"sosStatus": "site_status_sos",
				"address1": "address_street_1",
				"address2": "address_street_2",
				"city": "address_city",
				"state": "address_state",
				"postalCode": "address_zip",
				"residentFirstName": "resident_name_first",
				"residentLastName": "resident_name_last",
				"residentEmail": "resident_email",
				"homePhone": "resident_phone_home",
				"cellPhone": "resident_phone_cell",
				"homeRent": "rent_home",
				"currentRent": "rent_current",
				"marketRent": "rent_market",
				"securityDeposit": "rent_security_deposit",
				"isRental": "is_rental",
				"isRevenueOccupiedStatus": "is_revenue_occupied",
				"isVacantStatus": "is_vacant",
				"homeDetails": "home_details",
				"scheduledMoveoutDate": "moveout_scheduled_date",
			}
		),
		table="sites",
		method="drop",
		backup="dropbox",
		typeCatalogue={
			"home_details": "json",
		},
	)

	if (print_time):
		logger.logger_timer_print("sites")



@common.tryExcept
@logger.logger_timer("turnover")
def doTurnover(print_time=False):
	def modifyData_movein(data):
		""" Marks a row as a movein. """

		for row in data:
			row["is_movein"] = (row["sos_new"] in ("LTP - HH", "LTP", "RV - Occupied"))
		return data

	properties = database.posgres_raw(query_sql="SELECT property_id FROM property", as_dict=False)

	date_from = datetime.datetime.now()
	date_to = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=1)
	date_filter = f"fromYear={date_from.year}&fromMonth={date_from.month}&toYear={date_to.year}&toMonth={date_to.month}"

	database.posgres_insert(
		data=database.ma_getData(
			url=(f"https://n6.manageamerica.com/api/v1/residents/turnover/?propertyId={propertyId}&{date_filter}" for (propertyId,) in properties),
			login_user="VinApi",
			login_password="9@%sZqRxDeZ@38s",
			modifyData=modifyData_movein,
			alias={
				"firstName": "name_first",
				"groupId": "group_id",
				"lastName": "name_last",
				"propertyId": "property_id",
				"siteId": "site_id",
				"siteName": "site_name",
				"moveInDate": "movein_date",
				"moveInProcessedDate": "movein_processed_date",
				"moveOutDate": "moveout_date",
				"moveOutProcessedDate": "moveout_processed_date",
				"newSosStatus": "sos_new",
				"previousSosStatus": "sos_previous",
				"reasonDescription": "reason_description",
				"residentMoveOutReason": "reason_resident_moveout",
				"turnoverType": "turnover_type",
			},
		),
		table="turnover",
		method="drop",
		backup="dropbox",
	)

	if (print_time):
		logger.logger_timer_print("turnover")



@common.tryExcept
@logger.logger_timer("resident")
def doResident(print_time=False):
	# See: https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas/11354850#11354850
	# See: https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe/18145399#18145399
	frame = database.blobStorage_select(container="ma-extract", folder=("vineyards", "treehouse"), filename="Resident.csv")
	frame.rename({
		"Fiscal Month": "fiscal_month",
		"Fiscal Year": "fiscal_year",
		"Bus Unit Number": "bun",
		"MA Prop Code": "property_id",
		"Site ID": "site_id",
		"Resident ID": "resident_id",
		"Lease Description": "lease_description",
		"First Name": "name_first",
		"Last Name": "name_last",
		"Address1": "address_street_1",
		"Address2": "address_street_2",
		"City": "address_city",
		"State": "address_state",
		"Zip": "address_zip",
		"Phone": "phone",
		"Year Of Birth": "birthday_year",
		"Move In Date": "movein_date",
		"MI Reason": "movein_reason",
		"Move Out Date": "moveout_date",
		"MO Reason": "moveout_reason",
		"Addtl Occ Count": "occ_count_additional",
		"Current Or Former": "is_current_1",
		"Current Resident": "is_current_2",
		"EMail": "email",
		"Site Address": "site_address",
		"Site Type": "site_type",
		"SOS": "sos",
		"SOS After Moveout": "moveout_sos_after",
		"SOS Before Moveout": "moveout_sos_before",
		"Scheduled Move Out Date": "moveout_schedule_date",
		"Move In Process Date": "movein_process_date",
		"Move Out Process Date": "moveout_process_date",
		"Scheduled Move Out SOS": "moveout_schedule_sos",
		"Scheduled Move Out Removed": "moveout_schedule_removed",
		"Scheduled Move Out Reason": "moveout_schedule_reason",
		"Scheduled Move Out Comments": "moveout_schedule_comment",
		"Last Implemented Scheduled Rent Increase Date": "rent_increase_last_date",
		"Next Anticipated Rent Increase Date": "rent_increase_next_anticipated_date",
		"Next Scheduled Rent Increase Date": "rent_increase_next_schedule_date",
		"Use Billing Address": "address_use_billing_char",
		"Resident Group ID": "resident_group_id",
		"FICO Score": "score_fico",
		"Model Score": "score_model",
		"Lease Agreement Date": "lease_agree_date",
		"Lease Expiration Date": "lease_expire_date",
		"Total Monthly Housing Cost": "housing_cost_monthly_total",
	}, axis=1, inplace=True)
	frame.drop(["Q1 Base Rent", "Q1 Market Rent", "Q1 Market TMHC"], axis=1, inplace=True)
	frame["is_current"] = (frame.is_current_1 == "C")
	frame["address_use_billing"] = (frame.address_use_billing_char == "Y")

	database.posgres_insert(
		data=frame,
		table="resident",
		method="drop",
		backup="dropbox",
	)

	if (print_time):
		logger.logger_timer_print("resident")



@common.tryExcept
@logger.logger_timer("days_vacant")
def doDaysVacant(print_time=False):
	def modifyData_bools(data):
		""" Computes boolean columns from text columns. """

		for row in data:
			row["is_home_ready"] = row["is_home_ready_char"] in ("True", "Yes")

			for key in (
				"has_lot_prep",
				"has_concrete_flatwork",
				"has_block_and_level",
				"has_water_hookup",
				"has_sewer_hookup",
				"has_gas_hookup",
				"has_electric_hookup",
				"has_ac_installed",
				"has_step_installed",
				"has_deck_installed",
				"has_skirting_installed",
				"is_deck_finished",
				"is_electrical_finished",
				"is_exterior_paint_finished",
				"is_flooring_complete",
				"is_home_cleaned",
				"is_home_tashed_out",
				"is_interior_paint_finished",
				"is_kitchen_complete",
				"is_landscaping_finished",
				"is_plumbing_finished",
				"is_roof_finished",
				"is_smoke_detecor_working",
				"is_fire_extinguisher_available",
				"is_window_fixed",
				"is_lock_changed",
				"is_bathroom_finished",
				"is_appliance_working",
				"is_skirting_finished",
			):
				row[key] = (row[f"{key}_char"] == "Y")

		return data

	def modifyData_ensureType(data):
		""" Makes sure inputs are in the format postgres wants them to be in """

		# int
		for row in data:
			for key in (
				"days_in_community",
				"days_in_inventory",
				"days_vacant",
				"space_id",
			):
				row[key] = round(row[key] or 0)

		# date
		for row in data:
			for key in (
				"entered_community_date",
				"committed_home_ready_date",
				"refurb_completion_date",
				"refurb_start_date",
				"refurb_started_date",
				"refurb_completion_estimated_date",
			):
				value = row[key]
				if (not value):
					row[key] = None
					continue

				row[key] = datetime.datetime.strptime(value, r"%m/%d/%Y")

		return data

	database.posgres_insert(
		data=database.ma_getData(
			url="https://n6.manageamerica.com/api/addsReport/v1/runReport?Company_Id=233&Report_Id=3893",
			login_user="VinApi",
			login_password="9@%sZqRxDeZ@38s",
			customReport=True,
			alias={
				"Prop Code": "property_id",
				"Space Code": "space_id",
				"Home Id": "home_id",
				"Division": "division",
				"Region": "region",
				"Community": "community",
				"SOS": "sos",
				"Site": "site",
				"Serial Number1": "serial_number",
				"Days Home Vacant": "days_vacant",
				"Days In Community": "days_in_community",
				"Days In Inventory": "days_in_inventory",
				"Date Entered Community": "entered_community_date",
				"Committed Home Ready Date": "committed_home_ready_date",
				"Rehab Completion Date": "refurb_completion_date",
				"Rehab Start Date": "refurb_start_date",
				"Date Refurb Started": "refurb_started_date",
				"Rehab Estimated Completion Date": "refurb_completion_estimated_date",
				"Refurb Note": "refurb_note",
				"Lot Prep": "has_lot_prep_char",
				"Concrete Flatwork": "has_concrete_flatwork_char",
				"Block and Level": "has_block_and_level_char",
				"Water Hookup": "has_water_hookup_char",
				"Sewer Hookup": "has_sewer_hookup_char",
				"Gas Hookup": "has_gas_hookup_char",
				"Electric Hookup": "has_electric_hookup_char",
				"A/C Installed": "has_ac_installed_char",
				"Step(s) Installed": "has_step_installed_char",
				"Deck(s) Installed": "has_deck_installed_char",
				"Skirting Installed": "has_skirting_installed_char",
				"Home is Ready": "is_home_ready_char",
				"Is Deck/Steps Finished?": "is_deck_finished_char",
				"Is Electrical Finished?": "is_electrical_finished_char",
				"Is Exterior Paint Finished?": "is_exterior_paint_finished_char",
				"Is Flooring Complete?": "is_flooring_complete_char",
				"Is Home Cleaned?": "is_home_cleaned_char",
				"Is Home Trashed Out?": "is_home_tashed_out_char",
				"Is Interior Paint Finished?": "is_interior_paint_finished_char",
				"Is Kitchen Complete?": "is_kitchen_complete_char",
				"Is Landscaping Finished?": "is_landscaping_finished_char",
				"Is Plumbing Finished?": "is_plumbing_finished_char",
				"Is Roof Finished": "is_roof_finished_char",
				"Smoke/Carbon Detector Working?": "is_smoke_detecor_working_char",
				"Fire Extinguishers Available?": "is_fire_extinguisher_available_char",
				"Are Windows Fixed?": "is_window_fixed_char",
				"Are Locks Changed?": "is_lock_changed_char",
				"Are Bathrooms Finished?": "is_bathroom_finished_char",
				"Are Appliances Working?": "is_appliance_working_char",
				"Is Skirting Finished": "is_skirting_finished_char",
			},
			modifyData=[modifyData_bools, modifyData_ensureType],
		),
		table="days_vacant",
		method="drop",
		backup="dropbox",
	)

	if (print_time):
		logger.logger_timer_print("days_vacant")



@common.tryExcept
@logger.logger_timer("late_notice")
def doLateNotice(print_time=False):
	database.posgres_insert(
		data=database.fs_getData("rf1gmwaueh", view=101),
		table="late_notice",
		method="drop",
		backup="dropbox",
	)

	if (print_time):
		logger.logger_timer_print("late_notice")

def doAll():
	doProperty()
	doOccupancy()
	doSites()
	doTurnover()
	doResident()
	doDaysVacant()
	doLateNotice()
	logger.logger_timer_print()

def main():
	if not (len(sys.argv) > 1):
		return doAll()

	# See: https://docs.python.org/3/howto/argparse.html
	parser = argparse.ArgumentParser(description="Inserts data into postgres from various sources- mainly from Manage America")

	parser.add_argument("-a", 	"--all", 			action="store_true", help="Update all tables")
	parser.add_argument("-p", 	"--property", 		action="store_true", help="Update the property table")
	parser.add_argument("-o", 	"--occupancy", 		action="store_true", help="Update the occupancy table")
	parser.add_argument("-s", 	"--sites", 			action="store_true", help="Update the sites table")
	parser.add_argument("-t", 	"--turnover", 		action="store_true", help="Update the turnover table")
	parser.add_argument("-r", 	"--resident", 		action="store_true", help="Update the resident table")
	parser.add_argument("-v", 	"--days_vacant", 	action="store_true", help="Update the days_vacant table")
	parser.add_argument("-l", 	"--late_notice", 	action="store_true", help="Update the late_notice table")
	parser.add_argument(		"--log_subname", 						 help="What subname to use for the log file")

	args = parser.parse_args()

	if (args.all):
		return doAll()
	
	if (args.property):
		doProperty(print_time=True)
	
	if (args.occupancy):
		doOccupancy(print_time=True)
	
	if (args.sites):
		doSites(print_time=True)
	
	if (args.turnover):
		doTurnover(print_time=True)
	
	if (args.resident):
		doResident(print_time=True)
	
	if (args.days_vacant):
		doDaysVacant(print_time=True)
	
	if (args.late_notice):
		doLateNotice(print_time=True)

if (__name__ == "__main__"):
	logger.logger_info()
	# logger.logger_debug()
	main()
