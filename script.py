# Requirements
from urllib.parse import urlparse
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import config.config as config
from functions import *

# SQL Connection
connection = mysql.connector.connect(host=config.host,
                                    user=config.user,
                                    password=config.password,
                                    db=config.db)
cursor = connection.cursor(prepared=True)

# Loop over designated amount of pages
for page_number in range(1, 2):
    # Since tokens timeout every 10 minutes, go ahead and request a new token for each call
    token = refresh_api(config.client_id, config.client_secret, config.refresh_token)
    posts = get_data(page_number, token)
    
    for post in posts:
        print(post['author'])

cursor.close()
connection.close()


