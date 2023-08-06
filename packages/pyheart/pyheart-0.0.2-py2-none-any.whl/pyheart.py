import requests
import logging

def heartbeat(url):
    logging.basicConfig(filename='heartbeat.log', filemode='a', format='%(asctime)s - %(message)s')
    endpoint = '{}/heartbeat'.format(url) 
    ping = requests.get(endpoint, timeout=5)
    if ping.status_code == 200:
        logging.error('INFO: Server is up and running')
    else:
        logging.error('ERROR: Failed to reach server')
