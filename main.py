import math
import os
import json
import praw
import requests
import time
from RSSParser import find_newest_headline


class RedditBot:
    def __init__(self):
        # Initializes db dictionary, sets self.db
        self.db = self.load_db('db.json')
        # Loads config file, sets self.credentials and self.sub_list
        self.credentials, self.sub_list = self.load_config('config.json')
        print("Config:", self.credentials, self.sub_list)
        # Initializes reddit praw object
        self.reddit = praw.Reddit(username = self.credentials['user'],
                                password = self.credentials['password'],
                                client_id = self.credentials['client_id'],
                                client_secret = self.credentials['client_secret'],
                                user_agent = "Subreddit-News by /u/GeoWa")

    def load_config(self, config_file):
        # Loads the config file
        try:
            with open(config_file) as json_data_file:
                config = json.load(json_data_file)
                return config['credentials'], config['subreddits']
        except Exception as e:
            print(f'Error loading {config_file}: {str(e)}')

    def load_db(self, filename):
        # Loads the database file
        try:
            with open(filename) as file:
                return json.load(file)
        except Exception as e:
            print(f'Error loading {filename}: {str(e)}')
            print(f'Creating new {filename} file...')
            return {}

    def update_db(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.db, file, indent=4)

    def rss_request(self, url, last_modified=None, etag=None):
        try:
            resp = requests.get(url, headers={'If-Modified-Since': last_modified, 'If-None-Match': etag})
            if resp.ok:
                self.db["Last-Modified"] = resp.headers['Last-Modified']
                self.db["ETag"] = resp.headers['ETag']
                return resp.text
        except Exception as e:
            print(e)

    # Main Program Loop
    def main_loop(self):
        while True:
            print("Starting RSS feed...")

            next_update = int(math.inf)
            for sub_info in self.sub_list:
                print(f"Checking r/{sub_info['subreddit_name']} with {sub_info['rss_url']}...")
                key = sub_info['subreddit_name'] + sub_info['rss_url']
                if key not in self.db:
                    title, link, guid = find_newest_headline(requests.get(sub_info['rss_url']).text)
                    print("New story found! Making reddit post...")
                    new_update = int(time.time() + sub_info['delay'])
                    self.db[key] = {'last_id': guid, 'update_time': new_update}
                    if new_update < next_update:
                        next_update = new_update
                elif self.db[key]['update_time'] <= int(time.time()):
                    title, link, guid = find_newest_headline(requests.get(sub_info['rss_url']).text)
                    if self.db[key]['last_id'] == guid:
                        print("No new stories since last check")
                        new_update = self.db[key]['update_time'] + 300
                    else:
                        print("New story found! Making reddit post...")

                        new_update = int(self.db[key]['update_time'] + sub_info['delay'])
                    self.db[key]['update_time'] = new_update
                    if new_update < next_update:
                        next_update = new_update
                else:
                    if self.db[key]['update_time'] < next_update:
                        next_update = self.db[key]['update_time']

            # Update db.json
            print("Updating db.json...")
            self.update_db('db.json')
            break


if __name__ == "__main__":
    json.dump(int(time.time()), open('db.json', 'w'))
    # bot = RedditBot()
    # bot.main_loop()
