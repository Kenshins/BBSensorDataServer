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

    resp = requests.get(url=url,headers=headers)
    data = resp.json()
    logging.debug(data)
    return data

def request_sensor_temperature(sensor_id, token, address):
    headers = {'Authorization': 'Bearer ' + token}
    params = {'id': sensor_id}
    url = 'http://' + address + '/api' + '/sensor/info'

    resp = requests.get(url=url,params=params,headers=headers)
    data = resp.json()
    logging.debug(data)
    return data