# !/usr/bin/env python3

"""
This file starts the web server.
"""
import sys

from flask_login import LoginManager
from flask_mongoengine import MongoEngine

sys.path.append("..")

from config import FlaskConfig, Config

from flask_app.app import app

login_manager = LoginManager()

db = MongoEngine()

if __name__ == "__main__":

    app_kwargs = {
        'host': '127.0.0.1',
        'port': FlaskConfig.WEB_PORT,
        'debug': FlaskConfig.DEBUG,
    }

    app.config['MONGODB_SETTINGS'] = {'db': 'twitter_disaster_scraper',
                                      'host': Config.MONGODB_CONNECTION_STRING,
                                      'alias': 'default'}

    print(app.config['MONGODB_SETTINGS'])

    if FlaskConfig.DEBUG:

        # Verbose template loading.
        app.config.update({
            "EXPLAIN_TEMPLATE_LOADING": True,
        })

        # Use ad-hoc SSL.
        # This prevents us from having to create an SSL cert in development but still encrypts the connection.
        app_kwargs.update({
            "ssl_context": "adhoc",
        })

    else:  # Not debug mode, production mode.

        # Use SSL cert + key loaded from a file.
        app_kwargs.update({
            "ssl_context": (FlaskConfig.SSL_CERTIFICATE_PATH, FlaskConfig.SSL_KEY_PATH),
        })

    # Update app's config no matter what.
    app.config.update({
        'SECRET_KEY': FlaskConfig.SECRET_KEY,
    })

    db.init_app(app)

    # login_manager.init_app(app)

    app.run(**app_kwargs)
