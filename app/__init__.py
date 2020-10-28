from flask import Flask
from flaskappconfig import FlaskAppConfig
import pyrebase
import configuration
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(FlaskAppConfig)

app_config = configuration.config['appConfig']

firebase_config = configuration.config['firebaseConfig']
firebase = pyrebase.initialize_app(firebase_config)

serviceaccount_config = configuration.config['firebaseServiceaccount']

slack_config = configuration.config['slackConfig']

db = firebase.database()
auth = firebase.auth()
from app import routes
from app import kudobot
