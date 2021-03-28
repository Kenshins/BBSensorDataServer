#
#   Martin Kleberger 2021
#
#   Handle connection toward SQLite database
#

import sqlite3
import logging
from datetime import datetime

def setup_sqlite():
    connection = sqlite3.connect("sensor_data.db")
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
        cursor = connection.cursor()
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        cursor.execute('INSERT INTO sensor_data(id, timestamp, temp, humidity) VALUES (?,?,?,?)',
            (sensor_data['id'],timestamp, row[0]['value'], row[1]['value']))
        connection.commit()
    except sqlite3.IntegrityError:
         logging.debug('Row already exists')



