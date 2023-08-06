from flask import Flask, jsonify, session

from database import TweetResultDAO


def setup_api(app: Flask, tweetResultDAO: TweetResultDAO):
    """Sets up an HTTP API for Flask."""

    @app.route('/api/heartbeat/', methods=['GET'])
    def apiindex():
        resp = jsonify(success=True)
        resp.status_code = 200

        return resp

    @app.route('/api/database/tweets/count/', methods=['GET'])
    def databaseTweetCount():
        """Return the total number of saved tweets in the database."""
        return jsonify({'count': tweetResultDAO.get_number_tweets()})

    @app.route('/api/database/tweets/relevancy/breakdown', methods=['GET'])
    def databaseTweetCategorizations():
        """Return a per-tweet breakdown of relevant categories (UNCATEGORIZED, RELEVANT, etc)."""
        return jsonify(tweetResultDAO.get_relevancy_count())

    @app.route('/api/database/tweets/tags/breakdown/', methods=['GET'])
    def databaseTweetTags():
        """Return a per-tweet breakdown of tags saved in the database."""
        return jsonify(tweetResultDAO.get_popular_tags())

    @app.route('/api/session/indexTest/', methods=['GET'])
    def indexViews():
        """Return how many times the index page has been viewed."""
        return jsonify({'count': session.get('index_views', 0)})

    @app.route('/api/session/editTweet', methods=['GET'])
    def editTweet():
        """Return the tweet so that user can edit tags, relevancy."""
        return jsonify({'tweet': session.get('tweets_bag')})
