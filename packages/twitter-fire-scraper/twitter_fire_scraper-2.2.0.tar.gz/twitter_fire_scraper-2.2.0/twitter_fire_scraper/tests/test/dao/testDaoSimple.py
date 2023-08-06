import sys
sys.path.insert(1, 'C:/Users/Trung Pham/python/twitter-fire-scraper/code/twitter-fire-scraper/twitter_fire_scraper')

import unittest

from pymongo import MongoClient

from config import Config
from database.TweetResult import TweetResult, ERelevancy
from database.TweetResultDAO import TweetResultDAO
from tests.test.incur_api_hits.cached_tweets import CachedTweets


class TestDaoSimple(unittest.TestCase):

    def setUp(self) -> None:
        # connect to localhost
        self.client = MongoClient(Config.MONGODB_CONNECTION_STRING)

        # make a DAO with our connection
        self.dao = TweetResultDAO(self.client, collection_name=self.__class__.__name__)

    def tearDown(self) -> None:
        self.client.close()

    def testRealData(self):
        """Tests that the DAO can successfully insert and delete a few real records."""
        self.assertTrue(True)  # TODO

        # small amount of tweets
        tweetResultDict = CachedTweets.tweets_small()


        # save all of them
        for term, tweetResults in tweetResultDict.items():

            for tweetResult in tweetResults:

                # Make sure it doesn't already exist if we're running this SUPER fast or twice.
                if self.dao.get_by_id(tweetResult.get_id()) is not None:
                    self.dao.delete_by_id(tweetResult.get_id())

                self.dao.save_one(tweetResult)

        # using our local copy, retrieve them and compare them
        for term, tweetResults in tweetResultDict.items():

            for tweetResult in tweetResults:

                database_tweetResult = self.dao.get_by_id(tweetResult.get_id())

                # for brevity, compare their serialized forms.
                self.assertEqual(tweetResult.serialize(), database_tweetResult.serialize())

    def testMockData(self):
        """Tests that the DAO can successfully insert and delete a single mock record."""

        # delete if it somehow exists
        if self.dao.get_by_id('test_id') is not None:
            self.dao.delete_by_id('test_id')

        # mock tweetresult
        tweetResult = TweetResult(
            data={"id": "test_id",
                  "full_text": "hello!"},
            tags=["test", "deleteme"],
            relevancy=ERelevancy.IRRELEVANT)

        # save a tweetresult
        self.dao.save_one(tweetResult)

        # delete our local copy!
        del tweetResult

        # deserialize it from db
        database_result = self.dao.get_by_id("test_id")

        # It should exist
        self.assertNotEqual(database_result, None)

        # it should be of type TweetResult
        self.assertIsInstance(database_result, TweetResult)

        # it should have its tags,
        self.assertIn("test", database_result.tags)
        self.assertIn("deleteme", database_result.tags)

        # it should have its ERelevancy
        self.assertEqual(ERelevancy.IRRELEVANT, database_result.relevancy)

        # delete it now
        self.dao.delete_by_id(database_result.get_id())

        # it should be None since it's gone
        self.assertEqual(self.dao.get_by_id("test_id"), None)

    def test_Tags_Method(self):
        """
        Test if a DAO object can successfully add new tags or remove tags from a TwitterResult object.
        :return:
        """
        if self.dao.get_by_id('7') is not None:
            self.dao.delete_by_id('7')

        # mock tweetResult
        tweetResult = TweetResult(
            data={"id": "7",
                  "full_text": "The water at my house is contaminated!"},
            tags=["water"],
            relevancy=ERelevancy.RELEVANT)

        # save_one method
        self.dao.save_one(tweetResult)

        del tweetResult

        # get_by_id method
        mock_object = self.dao.get_by_id("7")

        # check that the object exits
        self.assertNotEqual(mock_object, None)

        # check that the object is of TweetResult type
        self.assertIsInstance(mock_object, TweetResult)

        # Add tags
        mock_object = self.dao.add_tags_by_id("7", "flood")

        # Test that new tag is in object
        self.assertIn("flood", mock_object.tags)

        # Remove tags
        mock_object = self.dao.remove_tags_by_id("7", "water")

        # Test that removed tag is not in object
        self.assertNotIn("water", mock_object.tags)

        self.dao.delete_by_id("7")