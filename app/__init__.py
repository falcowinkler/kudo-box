from flask import Flask

import configuration
from flaskappconfig import FlaskAppConfig

app = Flask(__name__)
app.config.from_object(FlaskAppConfig)

app_config = configuration.config['appConfig']

slack_config = configuration.config['slackConfig']

from app import routes
import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("dbname=kudos user=admin host=localhost password=admin")
# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("""CREATE TABLE kudos (
	kudo_id serial PRIMARY KEY,
	text VARCHAR ( 300 ) UNIQUE NOT NULL
);""")

print("hello")

if __name__ == '__main__':
    app.run()
