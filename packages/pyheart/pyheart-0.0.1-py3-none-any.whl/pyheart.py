import requests
import logging

def heartbeat(server):
    logging.basicConfig(filename='heartbeat.log', filemode='a', format='%(asctime)s - %(message)s')
    ping = requests.get(server, timeout=5)
    if ping.status_code == 200:
        logging.error('INFO: Server is up and running')
    else:
        logging.error('ERROR: Failed to reach server')
