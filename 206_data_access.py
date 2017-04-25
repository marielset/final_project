## Final Project Option 2
## Name: Mariel Setton

###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import random
import re 
import requests
from bs4 import BeautifulSoup
# Begin filling in instructions....

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_FNAME = "finalproject_caching.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

# store information in a cache file called finalproject_caching.json

## function to get and cache data from a twitter search term
def get_tweets_from_movie(movie):
    unique_identifier = "twitter_{}".format(movie)
    if unique_identifier in CACHE_DICTION:  
        twitter_results = CACHE_DICTION[unique_identifier]
    else:
        twitter_results = api.search(q=movie)
        CACHE_DICTION[unique_identifier] = twitter_results
        f = open(CACHE_FNAME,'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    # # print(twitter_results['statuses'])
    # for tweet in twitter_results['statuses']:
    #     print("TEXT:", tweet['text'])
    #     print("CREATED AT:", tweet['created_at'])
    #     print('')
    tweeter = [] # collect 'em all!
    for tweet in twitter_results["statuses"]:
        tweeter.append(tweet)
    return tweeter

# Get the data from all tweets containing the words beauty and the beast
movieData = get_tweets_from_movie("Beauty and the Beast")
# print(type(movieData))
# print(movieData[0])

def imdb_omdbapi(movietype):
    base_url = "http://www.omdbapi.com/?"
    unique_identifier = "omdb_{}".format(movietype)
    if unique_identifier in CACHE_DICTION:
        omdb_item = CACHE_DICTION[unique_identifier]
    else:
        param_diction = {}
        param_diction['t'] = movietype
        response = requests.get(base_url, params = param_diction)
        omdb_item = json.loads(response.text)
        CACHE_DICTION[unique_identifier] = omdb_item
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return omdb_item
info = imdb_omdbapi("Beauty and the Beast")
# print(info)

## your movie class with data about each movie in it
class Movie(object):
    def __init__(self, omdb_item):
        self.title = omdb_item["Title"]
        self.director = omdb_item["Director"]
        self.rating = float(omdb_item["imdbRating"])
        self.languages = omdb_item["Language"]
        self.descrip = omdb_item["Plot"]
        self.actor = omdb_item["Actors"]
        self.ID = omdb_item["imdbID"]

    # a function to print Beauty and the Beast by Disney (but not actually)
    def __str__(self):
        print('{} by {}'.format(str(self.title), str(self.director)))
    # a function to return a list of actors
    def grab_actors(self, amt = -1):
        actor_string = self.actor
        actor_list = actor_string.split(', ')
        # print(type(actor_list))
        # for i in actor_list:
            # print(i)
        if amt != -1:
            temp_list = actor_list
            actor_list = []
            for i in range(amt):
                actor_list.append(temp_list[i])
        return actor_list

# my_movie = Movie(info)
# #print(type(my_movie.actors()))
# ac_list = my_movie.actors()
# print(my_movie.rating)
# print(type(my_movie.rating))
# fake_list = my_movie.actors(2)
# print(len(fake_list))

class Tweeter(object):
    def __init__(self, tweet_item, movie):
        self.tweet = tweet_item
        self.text = tweet_item['text']
        self.ID = tweet_item['id']
        self.user_ID = tweet_item['user']['id']
        self.favs = tweet_item['favorite_count']
        self.user = tweet_item['user']['screen_name']
        self.retweets = tweet_item['retweet_count']
        self.movie = movie
        self.time = tweet_item['created_at']
        self.screen_name = tweet_item["user"]["screen_name"]
        self.num_favs = tweet_item["user"]["favourites_count"]
        self.user_mentions = tweet_item['entities']['user_mentions']
    def get_user_mentions(self):
        mention_list = ""
        for s in self.user_mentions:
            mention_list += s['screen_name']
            mention_list += " "
            # print(s['screen_name'])
            # print(s)
        return mention_list

# tweet_instance = Tweeter(movieData[1], my_movie)
# print(tweet_instance.text)

#list of the movie names
movie_names =  ["The Boss Baby", "Beauty and the Beast", "Moonlight", "Harry Potter and the Deathly Hallows: Part 2", "Zootopia", "Moana", "Finding Dory", "Dark Knight", "The BFG", "Lion"]

#list of the dictionaries of tweets
tweets_list = []
for tweet in movie_names:
    tweets_list.append(get_tweets_from_movie(tweet))

#list of tweet instances
tweet_instances = []
for s in range(len(tweets_list)):
    for i in tweets_list[s]:
        tweet_instances.append(Tweeter(i, movie_names[s]))

# print("Screen name = ", tweet_instances[0].screen_name)
# print("user mentions = ", tweet_instances[0].user_mentions)
listme = tweet_instances[0].get_user_mentions()
#list of the dictionaries of movies
movies_list = []
for movie in movie_names:
    movies_list.append(imdb_omdbapi(movie))

#list of movie instances
movie_instances = []
for movie in movies_list:
    movie_instances.append(Movie(movie))


## Create a database file with 3 tables:
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

# your Tweets table with 7 columns
cur.execute('DROP TABLE IF EXISTS Tweets')
table_spec = 'CREATE TABLE Tweets'
table_spec += '(tweet_id TEXT PRIMARY KEY, tweet_text TEXT, user_id TEXT, movie_search Movie, num_favs INTEGER, retweets INTEGER, user_mentions TEXT)'
cur.execute(table_spec)

# yout Users table with 3 columns
cur.execute('DROP TABLE IF EXISTS Users')
table_spec = 'CREATE TABLE Users'
table_spec += '(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER)'
cur.execute(table_spec)

# your Movies table with 6 columns
cur.execute('DROP TABLE IF EXISTS Movies')
table_spec = 'CREATE TABLE Movies'
table_spec += '(movie_id TEXT PRIMARY KEY, movie_title TEXT, movie_director TEXT, languages TEXT, IMDB_rating INTEGER, first_actor TEXT)'
cur.execute(table_spec)

# load data into your databases:

#load data into tweets table
for i in tweet_instances:
    listme = i.get_user_mentions()
    cur.execute('INSERT OR IGNORE INTO Tweets (tweet_id, tweet_text, user_id, movie_search, num_favs, retweets, user_mentions) VALUES (?, ?, ?, ?, ?, ?, ?)', (i.ID, i.text, i.user_ID, i.movie, i.favs, i.retweets, listme))

#load data into users table
for i in tweet_instances:
    cur.execute('INSERT OR IGNORE INTO Users (user_id, screen_name, num_favs) VALUES (?, ?, ?)', (i.user_ID, i.user, i.num_favs))

#load data into users table for user mentions
for i in tweet_instances:
    for j in i.user_mentions:
        unique_identifier = "user_{}".format(j['screen_name'])
        if unique_identifier in CACHE_DICTION:
            v = CACHE_DICTION[unique_identifier]
        else:
            v = api.get_user(j['screen_name']) 
            CACHE_DICTION[unique_identifier] = v
            f = open(CACHE_FNAME, 'w')
            f.write(json.dumps(CACHE_DICTION))
            f.close()
        cur.execute('INSERT OR IGNORE INTO Users (user_id, screen_name, num_favs) VALUES (?, ?, ?)', (v["id_str"], v["screen_name"], v["favourites_count"]))

# my_mov = Movie(Beauty_Beast_movie_data)
# lis = my_mov.actors(1)
# actor1 = lis[0]

# print(actor1)
# print(type(actor1))

#load data into movie table
for i in movie_instances:
    actors = i.grab_actors()
    cur.execute('INSERT OR IGNORE INTO Movies (movie_id, movie_title, movie_director, languages, IMDB_rating, first_actor) VALUES (?, ?, ?, ?, ?, ?)', (i.ID, i.title, i.director, i.languages, i.rating, actors[0]))


# find out which production companies are making the biggest movies tweeted about the most:
query = 'SELECT movie_search FROM Tweets WHERE retweets > 1000'
result = cur.execute(query)
movies = []
for s in result:
    # print("s = ", s[0])
    # print()
    movies.append(s)

# create a set so that you have one version of every movie mentioned
my_set = {s[0] for s in movies}

# create a dictionary of every movie and their directors
director_dict = {x.title : x.director for x in movie_instances}

# new_dict = {l:v for l, v in f}
# print(type(new_dict))
# for s in new_dict:
#     print(type(s))
#     print(s)
# for x in director_dict:
#     if x in my_set:
#         print (x)

# create a dictionary of every movie and their actor lists
actor_list = {x.title : x.grab_actors() for x in movie_instances}

# zip the movie, director and actors together
my_zip = zip(movie_names, director_dict.values(), actor_list.values())

zip_list = []
for z in my_zip:
    zip_list.append(z)

# filter the list to include only those that are in the movies.

f = filter(lambda x: x[0] in my_set, zip_list)

popular_movie_list = []
for l in f:
    popular_movie_list.append(l)

## create a dictionary of actors mapped to a dictionary of the director they worked for and how many times they worked for them
# start by looping through each movie and actor list
actor_dictionary = {}
for m in popular_movie_list:
    for act in m[2]:
        if act in actor_dictionary:
            if m[1] in actor_dictionary[act]:
                actor_dictionary[act][m[1]] += 1
            else:
                temp = {m[1] : 1}
                actor_dictionary[act] = temp
        else:
            temp = {m[1] : 1}
            actor_dictionary[act] = temp

# print(len(my_set))
# for t in range(len(my_set)):
#     m = my_set.pop()
#     print(m)

# find out if actors like to work with specific directors



conn.commit()


# keep this at the end of the code
conn.close()
# Put your tests here, with any edits you now need from when you turned them in with your project plan.
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
        m_dict = imdb_omdbapi("La La Land")
        moviename = Movie(m_dict)
        self.assertEqual(type(moviename), Movie)

    def test_2_str(self):
        m_dict = imdb_omdbapi("La La Land")
        mymovie = Movie(m_dict)
        words = mymovie.__str__();
        self.assertEqual(words, print("La La Land by Damien Chazelle"))

    def test_3_actor(self):
        m_dict = imdb_omdbapi("La La Land")
        mymovie = Movie(m_dict)
        my_list = mymovie.grab_actors()
        self.assertEqual(type(my_list), type(["hi", "the"]))

    def test_4_actor(self):
        m_dict = imdb_omdbapi("La La Land")
        mymovie = Movie(m_dict)
        my_list = mymovie.grab_actors(3)
        self.assertEqual(len(my_list), 3)

    def test_4_title(self):
        m_dict = imdb_omdbapi("La La Land")
        mymovie = Movie(m_dict)
        self.assertEqual(type(mymovie.title), type("La La Land"))

    def test_5_title(self):
        m_dict = imdb_omdbapi("La La Land")
        mymovie = Movie(m_dict)
        self.assertEqual(mymovie.title, "La La Land")

    def test_5_rating(self):
        m_dict = imdb_omdbapi("La La Land")
        mymovie = Movie(m_dict)
        self.assertEqual(type(mymovie.rating), type(5.0))

    def test_6_director(self):
        m_dict = imdb_omdbapi("La La Land")

class DatabadeTests(unittest.TestCase):
    def test_1_data_base(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tweets');
        result = cur.fetchall()
        self.assertTrue(len(result) >= 1, "Testing that the database is not empty")
        conn.close()



# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

if __name__ == "__main__":
    unittest.main(verbosity=2)
