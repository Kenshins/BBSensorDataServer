#
#   Martin Kleberger 2021
#
#   Temperature server. Fetching data from Telldus GW and send the data to the BBInformationServer
#

import time
import logging
import sys, getopt
import database_handler
import sensor_receiver
import sensor_data_publisher

def process_sensor_data(port, token, address, db_file):
    connection = database_handler.setup_sqlite(db_file)

    while True:
        sensors = sensor_receiver.request_sensors(token, address)
        logging.debug(sensors)
        database_handler.update_sensors(sensors, connection)

        for sensor in sensors['sensor']:
            sensor_data = sensor_receiver.request_sensor_temperature(sensor['id'], token, address)
            logging.debug(sensor_data)
            database_handler.update_sensor_data(sensor_data, connection)

        # Publish temperature and humidity update

        time.sleep(60)

def main(argv):
    port = 5555
    token = ""
    address = ""
    db_file = "sensor_data.db"
    
    try:
        opts, args = getopt.getopt(argv,"hp:t:n:d:",["port=", "token=", "telldus-address=", "database-file"])
    except getopt.GetoptError:
        print ('temp_server.py -p <port> -t <token> -n <telldus-address>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('temp_server.py -p <port>')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-t", "--token"):
            token = arg
        elif opt in ("-n", "--telldus-address"):
            address = arg
        elif opt in ("-d", "--database-file"):
            db_file = arg

    logging.basicConfig(level=logging.INFO)
    logging.info('Starting BBTempServer')
    process_sensor_data(port, token, address, db_file)

if __name__ == "__main__":
    main(sys.argv[1:])
