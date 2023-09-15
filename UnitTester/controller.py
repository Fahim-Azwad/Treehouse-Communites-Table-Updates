import sys
import random
import logging
import datetime
import unittest

import psycopg2
import pymsteams

sys.path.append("../PyUtilities")
import common
import logger
import database


# pip -m install
	# psycopg2
	# pymsteams

def sendTeamsHeartbeat(*, webhook=None):
	""" Lets MS Teams know it is running.

	Example Input: sendTeamsHeartbeat()
	"""

	if (logger.debugging):
		return

	logging.info("Sending heartbeat message to Teams...")

	webhook = webhook or database.config("webhook", "teams_unittest_heartbeat")
	teamsMessage = pymsteams.connectorcard(webhook)
	teamsMessage.title("Heartbeat")
	teamsMessage.text(random.choice((
		"Lorem ipsum dolor sit amet",
		"Leeroy Jenkins!!!!!!!!",
		"Checking stuff...",
		"Time to begin work!",
		"I'm here",
		"SIR!",
		"Alright, let's do this!",
		"Here to help!",
		"Present",
		"What will we come across this time?",
		"Here's to an uneventful program execution!",
		"At the ready!",
		"Reporting!",
		"Let's go!",
		"The hunt begins!",
		"SURPRISE!",
		"Ad astra abyssosque",
		"Uhn dara ma'nakai",
		"Raynor here",
		"Foul tarnished, in search of the Elden Ring. Emboldened by the flame of ambition. Someone must extinguish thy flame.",
		"Don't mind me",
		"bump",
	)))
	teamsMessage.send()

def sendTeamsError(error, title="Unknown Error", severity=None, *, webhook=None):
	""" Posts about an error on MS Teams
	See: https://pypi.org/project/pymsteams/
	Use: https://stackoverflow.com/questions/59371631/send-automated-messages-to-microsoft-teams-using-python/59371723#59371723

	Example Input: sendTeamsError(error)
	Example Input: sendTeamsError(error, "ACAP is Empty")
	"""

	if (logger.debugging):
		print(title)
		return

	webhook = webhook or database.config("webhook", "teams_unittest")
	teamsMessage = pymsteams.connectorcard(webhook)
	teamsMessage.title(title)

	match severity:
		# Use: https://colordesigner.io/gradient-generator
		case (None, 0):
			teamsMessage.color("#2196f3")

		case 1:
			teamsMessage.color("#927beb")

		case 2:
			teamsMessage.color("#d653c2")

		case 3:
			teamsMessage.color("#f81b7e")

		case _:
			teamsMessage.color("#F3212D")

	teamsMessage.text(str(error))

	logging.info(f"Teams Payload: '{teamsMessage.printme()}'")
	teamsMessage.send()

class BaseTest(unittest.TestCase):
	date_yesterday_andTwoHours = datetime.datetime.now() - datetime.timedelta(days=1, hours=2)
	date_threeHoursAgo = datetime.datetime.now() - datetime.timedelta(hours=3)
	date_oneHourAgo = datetime.datetime.now() - datetime.timedelta(hours=1)

def factory_blobFile(filename, container=None, *, minimum=None):
	""" A decorator function that tests if a blob container's file. If not- it warns MS Teams.

	Example Input: factory_blobFile("lorem.txt")
	Example Input: factory_blobFile("lorem.txt", "ipsum")
	Example Input: factory_blobFile("lorem.txt", minimum=BaseTest.date_oneHourAgo)
	"""

	container = container or "postgres"
	minimum = minimum or BaseTest.date_yesterday_andTwoHours
	
	def decorator(myFunction):
		@common.runOnFail(sendTeamsError, f"The blob file '{filename}' of the container '{container}' is not updating")
		def inner(self):
			logging.info(f"Testing '{filename}' in {container}...")
			self.assertGreaterEqual(self.getLatest(filename, container).replace(tzinfo=None), minimum)
		return inner
	return decorator

class TestBlobUpdated(BaseTest):
	""" Checks if a blob storage item has been recently updated. """

	@classmethod
	def setUpClass(cls):
		cls.catalogue_connection = {}

	def getConnection(self, container=None):
		""" Returns a connection for *container. Reuses connections that have already been made.

		Example Input: getConnection()
		Example Input: getConnection("lorem")
		"""

		container = container or "postgres"
		connection = self.catalogue_connection.get(container, None)
		if (connection is not None):
			return connection

		connection = database.BlobStorage.getConnection(container)
		self.catalogue_connection[container] = connection

		return connection

	def getLatest(self, filename, container=None):
		""" Returns the latest modified date from the blob *filename* in *container*.
		See: https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end/48340500#48340500

		Example Input: getLatest("lorem.txt")
		Example Input: getLatest("lorem.txt", "ipsum")
		"""

		container = container or "postgres"
		connection = self.getConnection(container)
		logging.info(f"Testing '{filename}' in {container}...")

		date_latest = database.BlobStorage.getMeta(
			container=container,
			filename=filename,
			output_type="client",
		)["last_modified"]
		
		logging.debug(logger.debugging and f"latest *date_modified* for '{filename}' of '{container}': '{date_latest:%Y/%m/%d at %H:%M:%S}'")
		return date_latest.replace(tzinfo=None)

	@factory_blobFile("vineyards/acapdetail.csv", "ma-extract")
	def test_py_maVineyards(self):
		pass

	@factory_blobFile("treehouse/acapdetail.csv", "ma-extract")
	def test_py_maVineyards(self):
		pass

	@factory_blobFile("sos/sos_codes_165.xlsx", "drilldowns")
	def test_pbiRobots_sos156(self):
		pass

	@factory_blobFile("sos/sos_codes_233.xlsx", "drilldowns")
	def test__pbiRobots_sos156(self):
		pass

	@factory_blobFile("sos/sos_codes_vacant.xlsx", "drilldowns")
	def test__pbiRobots_sosVacant(self):
		pass

	@factory_blobFile("rps/wtd_export_rps.xlsx", "drilldowns", minimum=BaseTest.date_threeHoursAgo)
	def test__pbiRobots_rpsWtd(self):
		pass

	@factory_blobFile("rps/mtd_export_rps.xlsx", "drilldowns", minimum=BaseTest.date_threeHoursAgo)
	def test__pbiRobots_rpsMtd(self):
		pass

	@factory_blobFile("inspections/inspections_vine.xlsx", "vine-kpis", minimum=BaseTest.date_threeHoursAgo)
	def test__pbiRobots_inspections(self):
		pass

	@factory_blobFile("inspections/full_list.xlsx", "vine-kpis", minimum=BaseTest.date_threeHoursAgo)
	def test__pbiRobots_inspectionsFull(self):
		pass

def factory_postgresTable(table, *, minimum=None):
	""" A decorator function that tests if a table has been updated. If not- it warns MS Teams.

	Example Input: factory_postgresTable("lorem")
	Example Input: factory_postgresTable("lorem", minimum=BaseTest.date_oneHourAgo)
	"""

	minimum = minimum or BaseTest.date_yesterday_andTwoHours
	def decorator(myFunction):
		@common.runOnFail(sendTeamsError, f"The postgres table '{table}' is not updating")
		def inner(self):
			logging.info(f"Testing {table} table...")
			self.assertGreaterEqual(self.getLatest(table), minimum)
		return inner
	return decorator

class TestPostgresUpdated(BaseTest):
	""" Checks if the postgres databbase has been recently updated. """

	@classmethod
	def setUpClass(cls):
		cls.connection = psycopg2.connect(**database.config())

	@classmethod
	def tearDownClass(cls):
		cls.connection.close()

	def getLatest(self, table):
		""" Returns the latest modified date from *table* in the postgres database

		Example Input: getLatest("late_notice")
		"""

		with self.connection as connection:
			with connection.cursor() as cursor:
				cursor.execute(f"SELECT max(date_modified) FROM {table}", ())
				date_latest = cursor.fetchone()[0]
				logging.debug(logger.debugging and f"latest *date_modified* for '{table}': '{date_latest:%Y/%m/%d at %H:%M:%S}'")
				return date_latest

	@factory_postgresTable("property")
	def test_property(self):
		pass

	@factory_postgresTable("occupancy")
	def test_occupancy(self):
		pass

	@factory_postgresTable("resident")
	def test_resident(self):
		pass

	@factory_postgresTable("days_vacant")
	def test_days_vacant(self):
		pass

	@factory_postgresTable("acap")
	def test_acap(self):
		pass

	@factory_postgresTable("late_notice", minimum=BaseTest.date_threeHoursAgo)
	def test_late_notice(self):
		pass

	@factory_postgresTable("turnover", minimum=BaseTest.date_oneHourAgo)
	def test_turnover(self):
		pass

if __name__ == '__main__':
	logger.logger_info(silence_urlib=True)
	# logger.logger_debug(silence_urlib=True)

	sendTeamsHeartbeat()
	# unittest.main()
	# sendTeamsError(ValueError("test"))