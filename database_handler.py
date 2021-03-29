#
#   Martin Kleberger 2021
#
#   Handle connection toward SQLite database
#

import sqlite3
import logging
from datetime import datetime

last_value = {}

def setup_sqlite(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('''create table if not exists sensors (id INTEGER PRIMARY KEY, timestamp REAL, model TEXT, name TEXT, novalues INTEGER, protocol TEXT, sensor_id INTEGER)''')
    cursor.execute('''create table if not exists sensor_data (id INTEGER, timestamp REAL, temp REAL, humidity REAL)''')
    return connection

def update_sensors(sensors, connection):
    cursor = connection.cursor()
    for sensor in sensors['sensor']:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        try:
            cursor.execute('INSERT INTO sensors(id, timestamp, model, name, novalues, protocol, sensor_id) VALUES (?,?,?,?,?,?,?)',
            (sensor['id'],timestamp, sensor['model'], sensor['name'], sensor['novalues'],
            sensor['protocol'], sensor['sensorId']))
        except sqlite3.IntegrityError:
            cursor.execute('UPDATE sensors SET timestamp=?, name=? where id=?', (timestamp,sensor['id'], sensor['name']))
    connection.commit()

def update_sensor_data(sensor_data, connection):
    try:
        row = sensor_data['data']
        id = sensor_data['id']
        temperature = row[0]['value']
        humidity = row[1]['value']

        if not id in last_value:
            last_value[id] = {'temp' : 0.0, 'hum' : 0.0}

        if (last_value[id]['temp'] != temperature or last_value[id]['hum'] != humidity):
            cursor = connection.cursor()
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            cursor.execute('INSERT INTO sensor_data(id, timestamp, temp, humidity) VALUES (?,?,?,?)',
                (id,timestamp, temperature, humidity))
            connection.commit()
            last_value[id] = {'temp' : temperature, 'hum' : humidity}
    except sqlite3.IntegrityError:
         logging.debug('Row already exists')



