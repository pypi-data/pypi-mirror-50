import csv
import os
import shutil
import tempfile
import unittest

from scraper import Scraper
from tests.test.incur_api_hits.cached_tweets import CachedTweets
from util import is_ascii


class TestFileSaving(unittest.TestCase):

    def count_statuses(self, statuses):
        total_statuses = 0
        for keyword, statuses in statuses.items():
            for status in statuses:
                total_statuses += 1

        return total_statuses

    def setUp(self):
        # Temp folder for CSV files
        self.temp_folder = os.path.join(tempfile.gettempdir(), "twitter_fire_scraper", TestFileSaving.__name__)

        # Scraper for scraping
        self.scraper = CachedTweets.scraper

        # Assorted filetype dirs
        self.csv_folder = os.path.join(self.temp_folder, 'csv')
        self.json_folder = os.path.join(self.temp_folder, 'json')

        os.makedirs(self.temp_folder, exist_ok=True)
        os.makedirs(self.csv_folder, exist_ok=True)
        os.makedirs(self.json_folder, exist_ok=True)

        print("Saved CSV files from test cases can be found at:")
        print(self.temp_folder)

    def testSaveCSVSmall(self):
        """Tests that the scraper can produce small CSV files."""
        tweets = CachedTweets.tweets_small_geo()

        tweets_csv_path = os.path.join(self.csv_folder, 'tweets_small.csv')

        self.scraper.save_tweetresultdict_to_csv(tweets, tweets_csv_path, overwrite=True)

        total_lines = 0
        with open(tweets_csv_path, 'r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=Scraper.CSV_DELIMITER)
            for row in csv_reader:
                total_lines += 1

        total_statuses = self.count_statuses(tweets)

        # We should have as many tweets as there are lines in the file, plus one for the header.
        self.assertEqual(total_lines, total_statuses + 1)

    def testSaveCSVNoRetweets(self):
        """Tests that the scraper can produce a CSV file with absolutely no retweets."""
        tweets = CachedTweets.tweets_medium_no_retweets()

        tweets_csv_path = os.path.join(self.csv_folder, 'tweets_medium_noretweets.csv')

        self.scraper.save_tweetresultdict_to_csv(tweets, tweets_csv_path, overwrite=True)

        total_lines = 0
        with open(tweets_csv_path, 'r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=Scraper.CSV_DELIMITER)
            for row in csv_reader:
                total_lines += 1

        total_statuses = self.count_statuses(tweets)

        # We should have as many tweets as there are lines in the file, plus one for the header.
        assert (total_lines == (total_statuses + 1))

    def testSaveCSVBlacklistedStrings(self):
        """Tests that the scraper can produce CSV files that blacklist certain strings."""
        tweets = CachedTweets.tweets_large_geo()
        banned_words = ['fire', 'flood', 'house fire', ' ']  # Yes, this is a single space, to be sure that it works.

        tweets_csv_path = os.path.join(self.csv_folder, 'tweets_large_blacklist_strings.csv')

        self.scraper.save_tweetresultdict_to_csv(tweets,
                                                 tweets_csv_path,
                                                 blacklisted_strings=banned_words,
                                                 overwrite=True)

        total_lines = 0
        with open(tweets_csv_path, 'r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=Scraper.CSV_DELIMITER)
            for row in csv_reader:
                total_lines += 1

                # For all banned words,
                for banned_word in banned_words:
                    # This row in the file should not contain the banned word.
                    self.assertNotIn(banned_word, row)

        total_statuses = self.count_statuses(tweets)

        # We should have as many tweets as there are lines in the file, plus one for the header.
        self.assertEqual(total_lines, (total_statuses + 1))

    def testSaveCSVOnlyASCIIWithArabic(self):
        """Tests that the scraper can produce CSV files that only contain ASCII while getting tweets in Arabic."""
        tweets = CachedTweets.tweets_small_arabic()

        tweets_csv_path = os.path.join(self.csv_folder, 'tweets_small_arabic_only_ASCII.csv')

        self.scraper.save_tweetresultdict_to_csv(tweets, tweets_csv_path, ascii_only=True, overwrite=True)

        total_lines = 0
        with open(tweets_csv_path, 'r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=Scraper.CSV_DELIMITER)
            for row in csv_reader:
                total_lines += 1

                # For all cells,
                for cell in row:
                    # For all single characters,
                    for character in cell:
                        # This character in the row should not contain non-ascii characters.
                        self.assertTrue(is_ascii(character))

        total_statuses = self.count_statuses(tweets)

        # We should have as many tweets as there are lines in the file, plus one for the header.
        self.assertEqual(total_lines, (total_statuses + 1))

    def testSaveCSVLarge(self):
        """Tests that the scraper can produce large CSV files."""
        tweets = CachedTweets.tweets_large_geo()

        tweets_csv_path = os.path.join(self.csv_folder, 'tweets_large.csv')

        self.scraper.save_tweetresultdict_to_csv(tweets, tweets_csv_path, overwrite=True)

        total_lines = 0
        with open(tweets_csv_path, 'r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=Scraper.CSV_DELIMITER)
            for row in csv_reader:
                total_lines += 1

        total_statuses = self.count_statuses(tweets)

        # We should have as many tweets as there are lines in the file, plus one for the header.
        self.assertEqual(total_lines, (total_statuses + 1))
