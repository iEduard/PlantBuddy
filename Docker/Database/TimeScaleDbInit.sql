/* Create the Relationable Table https://docs.timescale.com/timescaledb/latest/quick-start/python/#create-a-relational-table */
CREATE TABLE plants (id SERIAL PRIMARY KEY, type VARCHAR(50), location VARCHAR(50));

/* Create the Hypertable https://docs.timescale.com/timescaledb/latest/quick-start/python/#create-hypertable */
CREATE TABLE sensor_data ( time TIMESTAMPTZ NOT NULL, sensor_id INTEGER, sensor_name VARCHAR(50), light_intensity DOUBLE PRECISION, air_temperature DOUBLE PRECISION, soil_moisture DOUBLE PRECISION, soil_conductivity DOUBLE PRECISION, battery_level DOUBLE PRECISION, FOREIGN KEY (sensor_id) REFERENCES plants (id));

/* Select the created Hypertable */
SELECT create_hypertable('sensor_data', 'time');
