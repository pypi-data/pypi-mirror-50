# !/usr/bin/env python3

"""
This file starts the web server.
"""
import os
import sys

from flask import Flask
from flask_mongoengine import MongoEngine

from flask_app.http_forms import setup_http_routes
from flask_app.http_api import setup_api

current_folder = os.path.abspath(os.path.dirname(__file__))
static_folder = os.path.join(current_folder, 'static')
template_folder = os.path.join(current_folder, 'templates')

app = Flask(__name__, static_url_path='/static', template_folder=template_folder, static_folder=static_folder)

db = MongoEngine()
db.init_app(app)

from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from database.TweetResultDAO import TweetResultDAO

sys.path.append("..")

from config import FlaskConfig, Config

from scraper import Scraper

from twitter import TwitterAuthentication

scraper = Scraper(twitter_authentication=TwitterAuthentication.autodetect_twitter_auth())

login_manager = LoginManager(app)

tweetResultDao = TweetResultDAO()

if __name__ == "__main__":

    app_kwargs = {
        'host': '127.0.0.1',
        'port': FlaskConfig.HTTPS_PORT,
        'debug': FlaskConfig.DEBUG,
    }

    app.config['MONGODB_SETTINGS'] = {'db': 'twitter_disaster_scraper',
                                      'host': Config.MONGODB_CONNECTION_STRING,
                                      'alias': 'default'}

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

    login_manager.init_app(app)

    from database.User import User


    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()


    Bootstrap(app)

    setup_http_routes(app, scraper, tweetResultDao)

    setup_api(app, tweetResultDao)

    app.run(**app_kwargs)
