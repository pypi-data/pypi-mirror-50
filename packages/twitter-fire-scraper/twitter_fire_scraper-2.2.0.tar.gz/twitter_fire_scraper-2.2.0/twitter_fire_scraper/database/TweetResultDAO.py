from typing import Union, Dict, List

from pymongo import MongoClient
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database

from config import Config
from database.TweetResult import TweetResult


class TweetResultDAO(object):
    """
    A DAO that lets you save, modify, and retrieve TweetResults from the database.
    """

    def __init__(self, mongoclient: MongoClient = None, database_name='tweets', collection_name='all_tweets'):

        if mongoclient is None:
            mongoclient = MongoClient(Config.MONGODB_CONNECTION_STRING)

        self.client: MongoClient = mongoclient

        self.database_name = database_name
        self.db: Database = self.client[self.database_name]

        self.collection_name = collection_name
        self.collection: Collection = self.db[self.collection_name]

    def save_one(self, tweetresult: TweetResult):
        """Save a single TweetResult object."""
        self.collection.insert_one(tweetresult.serialize())

    def save_tweetresult_dict(self, tweetresultdict: Dict[str, List[TweetResult]]):
        """Save a Dict[str, List[TweetResult]] to the database."""
        for _, tweetresults in tweetresultdict.items():
            for tweetresult in tweetresults:
                self.save_one(tweetresult)

    def get_relevancy_count(self) -> List[Dict]:
        """Return a per-tweet breakdown of relevant categories (UNCATEGORIZED, RELEVANT, etc)."""
        cursor = self.collection.aggregate([
            {'$sortByCount': '$relevancy'}
        ])

        return [item for item in cursor]

    def get_popular_tags(self) -> List[Dict]:
        """Return a per-tweet breakdown of tags saved in the database."""
        cursor = self.collection.aggregate([
            {"$unwind": "$tags"},
            {'$sortByCount': '$tags'}
        ])

        return [item for item in cursor]

    def get_by_id(self, id) -> Union[TweetResult, None]:
        """Return a tweet by ID.

        Returns None if no tweet is found."""
        cursor = self.collection.find({"_id": id})

        if cursor.count() == 0:
            return None

        result = cursor.next()

        cursor.close()

        return TweetResult.deserialize(result)

    def delete_by_id(self, id):
        self.collection.delete_one({"_id": id})

    def add_tags_by_id(self, id, new_tags):
        """
        Add tags to a TweetResult object by ID.

        Return None if no tweet is found.
        """
        result = self.collection.find_one_and_update({"_id": id}, {'$addToSet': {'tags': new_tags}},
                                                     return_document=ReturnDocument.AFTER)
        print(result)

        return TweetResult.deserialize(result)

    def remove_tags_by_id(self, id, removed_tags):
        """
        Remove tags of a TweetResult object by ID
        :return: None if no tweets is found
                 TweetResult object (tags removed)
        """
        result = self.collection.find_one_and_update({"_id": id}, {'$pull': {'tags': removed_tags}},
                                                     return_document=ReturnDocument.AFTER)
        print(result)

        return TweetResult.deserialize(result)

    def get_number_tweets(self):
        """Get the number of saved tweets in the database."""
        return self.collection.count()

    def move_to_new_collection(self):
        """
        Move TweetResult object from one collection to another.
        Currently there's only 1 collection
        :return: None
        """
        raise NotImplementedError()

    def update_relevancy(self):
        """
        Update the relevancy metadata of TweetResult object.
        :return: updated TweetResult object
        """
        raise NotImplementedError()
