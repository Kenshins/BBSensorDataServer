#
#   Martin Kleberger 2021
#
#   Receive sensor data from Telldus Tellstick ZNET lite v2
#

import requests
import logging

def request_sensors(token, address):
    headers = {'Authorization': 'Bearer ' + token}
    url = 'http://' + address + '/api' + '/sensors/list'

    try:
        resp = requests.get(url,headers=headers,timeout=30)
    except Exception as err:
        logging.error("Exception raised when requesting data from Telldus gateway " + str(err))
        logging.error("Jumping this cycle")
        return None

    if resp.status_code is 200:
        data = resp.json()
        logging.debug(data)
        return data
    else:
        logging.error("Bad status code from requests.get")
        logging.error("Jumping this cycle")
        return None

def request_sensor_temperature(sensor_id, token, address):
    headers = {'Authorization': 'Bearer ' + token}
    params = {'id': sensor_id}
    url = 'http://' + address + '/api' + '/sensor/info'
    
    try:
        resp = requests.get(url,params=params,headers=headers,timeout=30)
    except Exception as err:
        logging.error("Exception raised when requesting data from Telldus gateway " + str(err))
        logging.error("Jumping this cycle")
        return None

    if resp.status_code is 200:
        data = resp.json()
        logging.debug(data)
        return data
    else:
        logging.error("Bad status code from requests.get")
        logging.error("Jumping this cycle")
        return None