#!/usr/bin/env python3

import pathlib
import sys
import re
import json
import threading
from time import sleep, localtime, strftime
from collections import OrderedDict
from colorama import init as colorama_init
from colorama import Fore, Back, Style
from unidecode import unidecode
from miflora.miflora_poller import MiFloraPoller, MI_BATTERY, MI_CONDUCTIVITY, MI_LIGHT, MI_MOISTURE, MI_TEMPERATURE
from btlewrap import BluepyBackend, BluetoothBackendException
from bluepy.btle import BTLEException
import sdnotify
import psycopg2
from datetime import datetime, timezone

## Class originated from: https://github.com/ThomDietrich/miflora-mqtt-daemon


if False:
	# will be caught by python 2.7 to be illegal syntax
	print('Sorry, this script requires a python3 runtime environment.', file=sys.stderr)


class PlantSensors():
	"""
	Read the Sensordata from ble and send them to an timescale db
	"""

	PARAMETERS = dict([
		(MI_LIGHT, dict(name="LightIntensity", name_pretty='Sunlight Intensity', typeformat='%d', unit='lux', device_class="illuminance", state_class="measurement")),
		(MI_TEMPERATURE, dict(name="AirTemperature", name_pretty='Air Temperature', typeformat='%.1f', unit='°C', device_class="temperature", state_class="measurement")),
		(MI_MOISTURE, dict(name="SoilMoisture", name_pretty='Soil Moisture', typeformat='%d', unit='%', device_class="humidity", state_class="measurement")),
		(MI_CONDUCTIVITY, dict(name="SoilConductivity", name_pretty='Soil Conductivity/Fertility', typeformat='%d', unit='µS/cm', state_class="measurement")),
		(MI_BATTERY, dict(name="Battery", name_pretty='Sensor Battery Level', typeformat='%d', unit='%', device_class="battery", state_class="measurement"))
	])

	def __init__(self, settingsPath="") -> None:
		"""
		Initialize the class
		"""
		self.readSensors = True

		#If no settings file passed use a default setting
		if settingsPath == "":
			settingsPath = str(pathlib.Path(__file__).parent.resolve()) + "/Settings/PlantSensors.json"


		# Systemd Service Notifications - https://github.com/bb4242/sdnotify
		self.sd_notifier = sdnotify.SystemdNotifier()

		# Intro
		colorama_init()
		print(Fore.GREEN + Style.BRIGHT)
		print(Style.RESET_ALL)
	
		# Read the settings to an local file
		_settings = self.__readSettings(settingsPath)

		self.settings_sensors = _settings["sensors"]

		used_adapter = _settings["general"].get("adapter", "hci0")

		self.daemon_enabled = _settings["deamon"].get("enabled", True)
		self.sleep_period = _settings["deamon"].get("period", 300)
		miflora_cache_timeout = self.sleep_period - 1

		#Get the TimeScale DB Configuration
		_sql_user = _settings["database"]["user"]
		_sql_password = _settings["database"]["password"]
		_sql_server = _settings["database"]["server"]
		_sql_port = _settings["database"]["port"]
		_sql_database = _settings["database"]["database"]
		self.TimeScaleDB_Connection = f"postgres://{_sql_user}:{_sql_password}@{_sql_server}:{_sql_port}/{_sql_database}"

		self.print_line('Configuration accepted', console=False, sd_notify=True)

		# Init the sensors
		self.floras = self.__initSensors(self.settings_sensors, miflora_cache_timeout = miflora_cache_timeout, used_adapter=used_adapter, sleep_period=self.sleep_period)

	def run(self)-> None:
		"""
		Start the Thread
		"""

		pass
		self.readSensors = True

		#Create a task and run it // , daemon=True
		self._sensorsDaemonThread = threading.Thread(target=self.__sensorsDaemon)
		self._sensorsDaemonThread.start()

	def __sensorsDaemon(self) -> None:
		"""
		Run the code
		"""

		self.sd_notifier.notify('READY=1')

		self.print_line('Initialization complete, starting MQTT publish loop', console=False, sd_notify=True)

		# Sensor data retrieval and publication
		while True:

			for [flora_name, flora] in self.floras.items():

				#Get the Data from the Sensor

				data = dict()
				attempts = 2
				flora['poller']._cache = None
				flora['poller']._last_read = None
				flora['stats']['count'] += 1
				self.print_line('Retrieving data from sensor "{}" ...'.format(flora['name_pretty']))

				while attempts != 0 and not flora['poller']._cache:
					try:
						flora['poller'].fill_cache()
						flora['poller'].parameter_value(MI_LIGHT)
					except (IOError, BluetoothBackendException, BTLEException, RuntimeError, BrokenPipeError) as e:
						attempts -= 1
						if attempts > 0:
							if len(str(e)) > 0:
								self.print_line('Retrying due to exception: {}'.format(e), error=True)
							else:
								self.print_line('Retrying ...', warning=True)
						flora['poller']._cache = None
						flora['poller']._last_read = None

				if not flora['poller']._cache:
					flora['stats']['failure'] += 1
					self.print_line('Failed to retrieve data from Mi Flora sensor "{}" ({}), success rate: {:.0%}'.format(
						flora['name_pretty'], flora['mac'], flora['stats']['success']/flora['stats']['count']
						), error = True, sd_notify = True)
					print()
					continue
				else:
					flora['stats']['success'] += 1

				for param,_ in self.PARAMETERS.items():
					data[param] = flora['poller'].parameter_value(param)
				self.print_line('Result: {}'.format(json.dumps(data)))


				try:
					#Write the Data to the Timescale DB
					with psycopg2.connect(self.TimeScaleDB_Connection) as conn:
						cursor = conn.cursor()

						# use the cursor to interact with your database
						sensor_id = flora["sensor_id"]
						sensor_name  = flora["name_pretty"]
						light_intensity = data.get("light")
						air_temperature = data.get("temperature")
						soil_moisture = data.get("moisture")
						soil_conductivity = data.get("conductivity")
						battery_level = data.get("battery")
						sql_timestamp = datetime.now(timezone.utc)

						sqlStatement = (f"INSERT INTO sensor_data (time, sensor_id, sensor_name, light_intensity, air_temperature,"
										f"soil_moisture, soil_conductivity, battery_level) VALUES (\'{sql_timestamp}\', {sensor_id}, \'{sensor_name}\', {light_intensity}," 
										f"{air_temperature}, {soil_moisture}, {soil_conductivity}, {battery_level});")

						#Execute the SQL Statement
						cursor.execute(sqlStatement)

						#Save the changes to the database
						conn.commit()

				except (Exception, psycopg2.Error) as error:
					print(error)

				print()

			self.print_line('Status messages published', console=False, sd_notify=True)

			if self.readSensors:
				self.print_line('Sleeping ({} seconds) ...'.format(self.sleep_period))
				sleep(self.sleep_period)
				print()
			else:
				self.print_line('Execution finished in non-daemon-mode', sd_notify=True)
				break

	def print_line(self, text, error = False, warning=False, sd_notify=False, console=True):
		"""
		# Logging function

		"""
		timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime())
		if console:
			if error:
				print(Fore.RED + Style.BRIGHT + '[{}] '.format(timestamp) + Style.RESET_ALL + '{}'.format(text) + Style.RESET_ALL, file=sys.stderr)
			elif warning:
				print(Fore.YELLOW + '[{}] '.format(timestamp) + Style.RESET_ALL + '{}'.format(text) + Style.RESET_ALL)
			else:
				print(Fore.GREEN + '[{}] '.format(timestamp) + Style.RESET_ALL + '{}'.format(text) + Style.RESET_ALL)
		timestamp_sd = strftime('%b %d %H:%M:%S', localtime())
		if sd_notify:
			self.sd_notifier.notify('STATUS={} - {}.'.format(timestamp_sd, unidecode(text)))

	def __initSensors(self, sensors, miflora_cache_timeout, used_adapter, sleep_period) -> dict:
		"""
		Initialize the plant sensors 
		"""
		# Initialize Mi Flora sensors
		flores = dict()

		for _sensor in sensors: 
			if not re.match("[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}", _sensor["mac"].lower()):
				self.print_line('The MAC address "{}" seems to be in the wrong format. Please check your configuration'.format(_sensor["mac"]), error=True, sd_notify=True)
				sys.exit(1)

			if '@' in _sensor["name"]:
				name_pretty, location_pretty = _sensor["name"].split('@')
			else:
				name_pretty, location_pretty = _sensor["name"], ''
			name_clean = self.__clean_identifier(name_pretty)
			location_clean = self.__clean_identifier(location_pretty)

			flora = dict()
			print('Adding sensor to device list and testing connection ...')
			print('Name:          "{}"'.format(name_pretty))


			flora_poller = MiFloraPoller(mac=_sensor["mac"], backend=BluepyBackend, cache_timeout=miflora_cache_timeout, adapter=used_adapter)
			flora['poller'] = flora_poller
			flora['name_pretty'] = name_pretty
			flora['mac'] = flora_poller._mac
			flora['refresh'] = sleep_period
			flora['location_clean'] = location_clean
			flora['location_pretty'] = location_pretty
			flora['stats'] = {"count": 0, "success": 0, "failure": 0}
			flora['firmware'] = "0.0.0"
			flora["sensor_id"] = _sensor["id"]
			try:
				flora_poller.fill_cache()
				flora_poller.parameter_value(MI_LIGHT)
				flora['firmware'] = flora_poller.firmware_version()
			except (IOError, BluetoothBackendException, BTLEException, RuntimeError, BrokenPipeError) as e:
				self.print_line('Initial connection to Mi Flora sensor "{}" ({}) failed due to exception: {}'.format(name_pretty, _sensor["mac"], e), error=True, sd_notify=True)
			else:
				print('Internal name: "{}"'.format(name_clean))
				print('Device name:   "{}"'.format(flora_poller.name()))
				print('MAC address:   {}'.format(flora_poller._mac))
				print('Firmware:      {}'.format(flora_poller.firmware_version()))
				self.print_line('Initial connection to Mi Flora sensor "{}" ({}) successful'.format(name_pretty, _sensor["mac"]), sd_notify=True)
				if int(flora_poller.firmware_version().replace(".", "")) < 319:
					self.print_line('Mi Flora sensor with a firmware version before 3.1.9 is not supported. Please update now.'.format(name_pretty, _sensor["mac"]), error=True, sd_notify=True)

			print()
			flores[name_clean] = flora

		return flores

	def __clean_identifier(self, name) -> str:
		"""
		Clean the name from special chars
		"""

		clean = name.strip()
		#Replace special schars from name
		for this, that in [[' ', '-'], ['ä', 'ae'], ['Ä', 'Ae'], ['ö', 'oe'], ['Ö', 'Oe'], ['ü', 'ue'], ['Ü', 'Ue'], ['ß', 'ss']]:
			clean = clean.replace(this, that)
		clean = unidecode(clean)
		return clean

	def __readSettings(self, settingsPath : str) -> dict:
		"""
		## read the settings and store them in an dictionary

		This method will read a json file to an dictionary

		- settingsPath : str = Settings source path as string
		"""

		settingsJson = {}

		#Read the configuration file 
		with open(settingsPath, "r") as settingsFile:
			settingsJson = json.load(settingsFile)


		#validate the settings
		#Validate the JSON file with an scheme
		# - - - To be done - - - 

		return settingsJson



if __name__ == "__main__":
	"""
	Main entry point
	"""

	sensorCollector = PlantSensors()
	sensorCollector.run()
	