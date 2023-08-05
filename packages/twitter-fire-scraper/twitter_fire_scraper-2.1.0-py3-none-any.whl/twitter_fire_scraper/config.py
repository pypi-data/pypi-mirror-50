import json
import os
import sys


def get_property_from_json_file(filepath, property):
    """Given a filepath pointing to a JSON file and a property, return the property stored in that JSON file."""

    if not os.path.exists(filepath):
        raise Exception("The file at '{}' does not exist!".format(
            filepath
        ))

    with open(filepath, 'r') as f:
        data = json.load(f)
        if property not in data:
            raise ValueError("Could not find the '{}' key inside of the file located at '{}'!".format(
                property, filepath
            ))
        else:
            return data[property]


class _Config(object):
    """
    This class stores configuration information like config file paths, default values, etc.
    """

    @staticmethod
    def example_mongodb_config():
        """
        :return: An example MongoDB configuration file as a string.
        """
        return json.dumps({
            'mongodb_connection_string': "mongodb://localhost:27017/",
        }, indent=4, sort_keys=True)

    @staticmethod
    def example_secrets_json():
        # type: () -> str
        """
        :return: An example of what the secrets.json configuration file should look like.
        """
        return json.dumps({
            'consumer_key': 'ABCDEFG_I_WOULD_LIKE_YOU_TO_REPLACE_ME',
            'consumer_secret': 'ABCDEFG_I_WOULD_LIKE_YOU_TO_REPLACE_ME',
            'access_token': 'ABCDEFG_I_WOULD_LIKE_YOU_TO_REPLACE_ME',
            'access_token_secret': 'ABCDEFG_I_WOULD_LIKE_YOU_TO_REPLACE_ME',
        }, indent=4, sort_keys=True)

    def create_example_secrets(self):
        """Create an example file that serves as `secrets.json` for the user to populate."""

        if not os.path.exists(self.CONFIG_FOLDER):
            os.mkdir(self.CONFIG_FOLDER)

        if not os.path.exists(self.SECRETS_DATAFILE_EXAMPLE_PATH):
            with open(self.SECRETS_DATAFILE_EXAMPLE_PATH, 'w') as f:
                f.write(self.example_secrets_json())

    def __init__(self):

        self.CONFIG_FOLDER = os.path.abspath(os.path.expanduser("~/.twitterfirescraper"))
        """The folder that configuration files, secrets, etc. get stored in."""

        if not os.path.exists(self.CONFIG_FOLDER):
            os.mkdir(self.CONFIG_FOLDER)

        self.SECRETS_DATAFILE_PATH = os.path.join(self.CONFIG_FOLDER, "secrets.json")
        """The file that stores Twitter API keys."""

        self.SECRETS_DATAFILE_EXAMPLE_PATH = os.path.join(self.CONFIG_FOLDER, "secrets.example.json")
        """The file that serves as an example of the secrets datafile."""

        self.CONFIG_FILE = os.path.join(self.CONFIG_FOLDER, "config.json")
        """The file that stores configuration such as rate limiting, API ports, etc."""

        self.API_PORT = 3620
        """The port the HTTP API exposing the Scraper object's functions operates in."""

        self.MONGODB_DATAFILE_PATH = os.path.join(self.CONFIG_FOLDER, "mongodb.json")
        """The file that stores MongoDB configuration information."""

        # Create configuration file that stores MongoDB configuration information if it doesn't exist
        if not os.path.exists(self.MONGODB_DATAFILE_PATH):
            with open(self.MONGODB_DATAFILE_PATH, 'w') as f:
                f.write(self.example_mongodb_config())

        self.MONGODB_CONNECTION_STRING = get_property_from_json_file(self.MONGODB_DATAFILE_PATH, 'mongodb_connection_string')
        """The connection string for the MongoDB server."""

# Instantiate class for easy importing.
Config = _Config()

class FlaskConfig:
    DEBUG = True
    """Whether or not the app is in DEBUG mode. Should never be TRUE in prod."""

    WEB_PORT = 443
    """The port the website runs on."""

    SSL_CERTIFICATE_PATH = os.path.join(Config.CONFIG_FOLDER, "cert.pem")
    """The location of the SSL certificate."""

    SSL_KEY_PATH = os.path.join(Config.CONFIG_FOLDER, "key.pem")
    """The location of the SSL key."""

    SECRET_KEY = "you will never guess :)"
    """A secret value Flask uses to encrypt session variables. Essentially an encryption key."""

    # If in prod,
    if DEBUG == False:

        SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

        # If there is no flask secret key,
        if SECRET_KEY is None:
            raise ValueError(
                "No environment variable called `FLASK_SECRET_KEY`! This is required for secure sessions and forms!")


def try_get(object, key):
    """Tries to get the value of a key in an object, and politely notifies you if it cannot find it."""

    if key not in object:
        raise KeyError("Could not find " + key + " inside of " + object + "! Does it exist?")

    return object[key]


class DataConfig:
    """Holds data and filepath configuration information for data files such as state names, hashtags we wish to track,
    terms that indicate fires or disasters, etc."""

    # Folder name that data is stored in.
    DATA_FOLDER_NAME = "data"

    # Path data is stored in.
    DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATA_FOLDER_NAME)

    # Disaster hashtag datafile location.
    DISASTER_HASHTAGS_DATA_PATH = os.path.join(DATA_PATH, "DisasterHashtags.yml")

    # Fire hashtag datafile location.
    FIRE_HASHTAGS_DATA_PATH = os.path.join(DATA_PATH, "FireHashtags.yml")

    # US major cities datafile location.
    MAJOR_CITIES_DATA_PATH = os.path.join(DATA_PATH, "MajorCities.yml")

    # US states datafile location.
    US_STATES_DATA_PATH = os.path.join(DATA_PATH, "USStates.yml")

    TWITTER_ACCOUNTS_DATA_PATH = os.path.join(DATA_PATH, "TwitterAccounts.yml")
