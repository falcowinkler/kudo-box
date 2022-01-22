from flask import Flask

import configuration
from flaskappconfig import FlaskAppConfig

app = Flask(__name__)
app.config.from_object(FlaskAppConfig)

app_config = configuration.config['appConfig']

slack_config = configuration.config['slackConfig']

from app import routes
