
from datetime import datetime, timezone
import psycopg2
import json



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




	def sendSensorData(self, sensorId:str, sensorName:str, data:dict):

		#Get the TimeScale DB Configuration
		self.TimeScaleDB_Connection = f"postgres://{self.user}:{self.password}@{self.server}:{self.port}/{self.database}"

		try:
			#Write the Data to the Timescale DB
			with psycopg2.connect(self.TimeScaleDB_Connection) as conn:

				# use the cursor to interact with your database
				cursor = conn.cursor()

				sqlTimestamp = datetime.now(timezone.utc)

				sqlStatement = (f"INSERT INTO sensor_data (time, sensor_id, sensor_name, data)"
								f" VALUES (\'{sqlTimestamp}\', {sensorId}, \'{sensorName}\', \'{json.dumps(obj=data,  indent=4)}\');")

				#Execute the SQL Statement
				cursor.execute(sqlStatement)

				#Save the changes to the database
				conn.commit()

		except (Exception, psycopg2.Error) as error:
			print(error)