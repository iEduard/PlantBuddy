

import psycopg2



class Database:
	"""
	Interface for the postgress SQL Database
	"""


	def __init__(self, user:str, password:str, server:str, port:str, database:str) -> None:
		"""
		Initialize the connection settings. Will create the connection key

		Params
		------
		user:str			= User of the PostgreSql Database 
		password:str		= Password of the PostgreSql user
		server:str			= Server Address. Can be ip or host name
		port:str			= Port of the PostgreSql Server
		database:str		= Name of the PostgreSql Table to use
		"""

		#Define the local variables
		self.user = user 
		self.password = password
		self.server = server
		self.port = port
		self.database = database



	def sendData(self, sensorId:str):

		#Get the TimeScale DB Configuration
		self.TimeScaleDB_Connection = f"postgres://{self.user}:{self.password}@{self.server}:{self.port}/{self.database}"

		try:
			#Write the Data to the Timescale DB
			with psycopg2.connect(self.TimeScaleDB_Connection) as conn:
				cursor = conn.cursor()

				# use the cursor to interact with your database
				sensor_id = sensorId
				sensor_name  = flora["name_pretty"]
				light_intensity = data.get("light")
				air_temperature = data.get("temperature")
				soil_moisture = data.get("moisture")
				soil_conductivity = data.get("conductivity")
				battery_level = data.get("battery")
				sql_timestamp = datetime.now(timezone.utc)

				sqlStatement = (f"INSERT INTO sensor_data (time, sensor_id, sensor_name, light_intensity, air_temperature,"
								f"soil_moisture, soil_conductivity, battery_level) VALUES (\'{sql_timestamp}\', {sensorId}, \'{sensor_name}\', {light_intensity}," 
								f"{air_temperature}, {soil_moisture}, {soil_conductivity}, {battery_level});")

				#Execute the SQL Statement
				cursor.execute(sqlStatement)

				#Save the changes to the database
				conn.commit()

		except (Exception, psycopg2.Error) as error:
			print(error)