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
        time.sleep(60)
        sensors = sensor_receiver.request_sensors(token, address)
        if sensors is None:
            continue

        logging.debug(sensors)
        database_handler.update_sensors(sensors, connection)

        for sensor in sensors['sensor']:
            sensor_data = sensor_receiver.request_sensor_temperature(sensor['id'], token, address)
            if sensors is None:
                continue

            logging.debug(sensor_data)
            database_handler.update_sensor_data(sensor_data, connection)

def main(argv):
    port = 5555
    token = ""
    address = ""
    db_file = "sensor_data.db"
    debug = False
    
    try:
        opts, args = getopt.getopt(argv,"hp:t:n:d::v::",["port=", "token=", "telldus-address=", "database-file", "verbose"])
    except getopt.GetoptError:
        print ('temp_server.py -p <port> -t <token> -n <telldus-address> -v <verbose>')
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
        elif opt in ("-v", "--verbose"):
            debug = True

    if (debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        
    logging.info('Starting BBTempServer')
    logging.debug('\nZeroMQ port: %s \ntoken: %s \naddress: %s \ndb_file: \n%s debug: %s' % (port, token, address, db_file, debug))
    process_sensor_data(port, token, address, db_file)

if __name__ == "__main__":
    main(sys.argv[1:])
