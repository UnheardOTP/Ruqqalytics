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

# Purge data from database
sql = "DELETE FROM tblSiteContent"
cursor.execute(sql)

# Loop over designated amount of pages
for page_number in range(1, 2):
    # Since tokens timeout every 10 minutes, go ahead and request a new token for each call
    token = refresh_api(config.client_id, config.client_secret, config.refresh_token)
    posts = get_data(page_number, token)
    
    for post in posts:
        try:
            url = post['url']
            submitter = post['author']
            source = urlparse(url).netloc
            # Strip url of WWW
            if "www." in source:
                source = source.replace('www.','')
            title = post['title']
            score = post['score']
            guild = post['guild_name']
            submitted = datetime.fromtimestamp(post['created_utc']).strftime("%Y-%m-%d %H:%M:%S")
            # Ensure the post is for a website and not for an internal ruqqus page
            if "http" in url:
                sql = """INSERT INTO tblSiteContent 
                        (url, title, source, score, submitter, submitted, guild, site) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                sql_values = (url,title,source,score,submitter,submitted,guild,"ruqqus")
                cursor.execute(sql, sql_values)
        except Exception as err:
            print(err)
            # Data isn't mission critical, so if we have to drop a record or two, no biggie
            pass
        connection.commit()

cursor.close()
connection.close()


