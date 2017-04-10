## Your name: Mariel Setton
## The option you've chosen: project 2!

# Put import statements you expect to need here!


import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import random
import re 
from bs4 import BeautifulSoup

# write a twitter class to gather information and store it in a cache file called finalproject_caching.json
# make sure to also store data in a twitter.db database where you can submit queries to

# write a movie class here with all the methods described

# process all the data in the end to output what is necessary

# good luck!!!!!


# Write your test cases here.
class CachingTests(unittest.TestCase):
    def test_cache_diction(self):
        self.assertEqual(type(CACHE_DICTION), type({}))

    def test_cache_file(self):
        f = open("finalproject_caching.json","r")
        s = f.read()
        f.close()
        self.assertEqual(type(s), type("mariel"))

class MovieTests(unittest.TestCase):
    def test_1_init(self):
        moviename = Movie(m_dict)
        self.assertEqual(type(moviename), Movie)

    def test_2_str(self):
        mymovie = Movie(movie_dict)
        words = mymovie.__str__();
        self.assertEqual(type(words), type("mariel"))

    def test_3_actor(self):
        mymovie = Movie(m_dict)
        my_list = mymovie.actor(3)
        self.assertEqual(type(my_list), type(["hi", "the"]))

    def test_4_actor(self):
        mymovie = Movie(m_dict)
        my_list = mymovie.actor(3)
        self.assertEqual(len(my_list), 3)

    def test_4_title(self):
        mymovie = Movie(m_dict)
        self.assertEqual(type(mymovie.title), type("mariel"))

    def test_5_rating(self):
        mymovie = Movie(m_dict)
        self.assertEqual(type(mymovie.rating), type(5))

## Remember to invoke all your tests...

if __name__ == "__main__":
    unittest.main(verbosity=2)


