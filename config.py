import logging
import configparser
from datetime import datetime

# Logger
log_name = str(datetime.today().strftime('%d-%m-%Y'))
logging.basicConfig(filename=f'twitchapi-{log_name}.log',
                    filemode='w',
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt='%D %H:%M:%S', 
                    level=logging.INFO)  # DEBUG / INFO

# Config
try:
    config = configparser.RawConfigParser()
    config.read('twitch.cfg')
    account = config.get('twitch', 'account')
    oauth_chat = config.get('twitch', 'oauth_chat')
    channel = config.get('twitch', 'channel')
    access_token = config.get('twitch', 'access_token')
    client_id = config.get('twitch', 'client_id')
    logging.info('Config loaded.')
except FileNotFoundError:
    logging.error('Config file not found.')
    print('Config file not found.')
    quit()
except configparser.NoSectionError:
    print("Corrupted config or no config file present.")
    logging.error("Corrupted config or no config file present.")
    quit()