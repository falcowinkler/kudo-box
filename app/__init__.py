from flask import Flask
from flaskappconfig import FlaskAppConfig
import pyrebase
import configuration

import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
app.config.from_object(FlaskAppConfig)

app_config = configuration.config['appConfig']

serviceaccount_config = configuration.config['firebaseServiceaccount']

slack_config = configuration.config['slackConfig']

cred = credentials.Certificate(serviceaccount_config)
firebase_admin.initialize_app(cred, {
    'databaseURL': f"https://{serviceaccount_config['project_id']}.firebaseio.com"
})

from app import kudobot
from app import routes
