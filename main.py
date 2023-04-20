from datetime import datetime
import argparse
import math
import time
import sys

import praw
import requests
from pprint import pprint

from file_manager import load_config, load_db, update_db
from notif import send_discord_message
from pause import until
from rss_parser import find_newest_headline


class RedditBot:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"

    def __init__(self, testing):
        # Sets testing mode
        self.testing = testing
        print(f"Testing Mode: {'ON' if self.testing else 'OFF'}")
        # Loads config file, sets self.credentials and self.sub_list
        self.sub_list, self.credentials = load_config('config.yaml')
        print("Config List:")
        pprint(self.sub_list)
        print("")
        # Initializes db dictionary, sets self.db
        self.db = load_db('db/db.json')
        self.initialize_db()
        # Initializes reddit praw object
        self.reddit = praw.Reddit(username=self.credentials['user'], password=self.credentials['password'],
                                  client_id=self.credentials['client_id'],
                                  client_secret=self.credentials['client_secret'],
                                  user_agent="Subreddit-News:V1.0 by /u/GeoWa")
        # Sends Discord Notification
        send_discord_message(
            f"Bot Started on {'Testing Mode' if self.testing else 'Normal Mode'} at {time.strftime('%Y-%m-%d %H:%M')}")

    def initialize_db(self):
        try:
            for sub_info in self.sub_list:
                if sub_info['name'] not in self.db:
                    self.db[sub_info['name']] = {
                        'update_list': [{"update_time": 0, "update_index": 0, "listening": True}] * len(
                            sub_info['rss_feeds']), 'rss_sources': {}}
                else:
                    db_entry = self.db[sub_info['name']]
                    if len(db_entry['update_list']) > len(sub_info['rss_feeds']):
                        db_entry['update_list'] = db_entry['update_list'][:len(sub_info['rss_feeds'])]
                    for index, item in enumerate(db_entry['update_list']):
                        item['update_time'] = min(item['update_time'],
                                                  int(time.time()) + sub_info['rss_feeds'][index]['check_interval'])
                        item['update_index'] = item['update_index'] if item['update_index'] < len(
                            sub_info['rss_feeds'][index]['urls']) else 0
                    total_urls = [url for feed in sub_info['rss_feeds'] for url in feed['urls']]
                    new_rss_sources = {}
                    for url in db_entry['rss_sources'].keys():
                        if url in total_urls:
                            new_rss_sources[url] = db_entry['rss_sources'][url]
                    db_entry['rss_sources'] = new_rss_sources
        except Exception as e:
            print(f'Unable to read the db: {str(e)}')
            print("The file might be corrupted, try deleting db.json then try again.")
            sys.exit(1)

    def rss_request(self, url, subreddit):
        try:
            db_entry = self.db[subreddit]['rss_sources'][url]
            resp = requests.get(url,
                                headers={'User-Agent': self.USER_AGENT, 'If-Modified-Since': db_entry['last_modified'],
                                         'If-None-Match': db_entry['etag']})
            if resp.status_code == 200:
                db_entry['last_modified'] = resp.headers['Last-Modified'] if 'Last-Modified' in resp.headers else None
                db_entry['etag'] = resp.headers['ETag'] if 'ETag' in resp.headers else None
                return resp.text
            else:
                return None
        except Exception as e:
            print(f'Error requesting {url}: {str(e)}')

    def subreddits_loop(self):
        next_update = math.inf  # next_update is the time in seconds until the next update
        for sub_info in self.sub_list:
            print(f"Checking r/{sub_info['name']}...")
            updates = self.db[sub_info['name']]['update_list']
            sources = self.db[sub_info['name']]['rss_sources']
            for index in range(len(sub_info['rss_feeds'])):
                current_feed = sub_info['rss_feeds'][index]
                update_entry = updates[index]
                url = current_feed['urls'][update_entry['update_index']]
                # New entry
                if url not in sources:
                    sources[url] = {'last_modified': None, 'etag': None}
                    update_entry['listening'] = True
                    print(f"Listening to {url}...")
                    response_text = self.rss_request(url, sub_info['name'])
                    if response_text:
                        new_update = math.ceil(time.time()) + 1800  # Check 30 minutes later
                        sources[url]['last_id'] = find_newest_headline(response_text)[2]
                        update_entry['update_time'] = new_update
                        next_update = min(new_update, next_update)
                # Update time has passed
                elif update_entry['update_time'] <= math.ceil(time.time()):
                    response_text = self.rss_request(url, sub_info['name'])
                    if not response_text:
                        print(f"No new data from {url}, continuing to listen")
                        new_update = int(time.time()) + 1800  # Check 30 minutes later
                        next_update = min(new_update, next_update)
                        update_entry.update({'update_time': new_update, 'listening': True})
                        continue
                    title, link, guid = find_newest_headline(response_text)
                    # Check for errors from RSSParser.py
                    if not title:
                        continue
                    if not update_entry['listening']:
                        print(f"Began listening")
                        new_update = int(time.time()) + 1800  # Check 30 minutes later
                        sources[url]['last_id'] = guid
                        update_entry.update({'update_time': new_update, 'listening': True})
                    elif sources[url]['last_id'] == guid:
                        print(f"No new stories from {url}")
                        new_update = int(time.time()) + 1800  # Check 30 minutes later
                        update_entry.update({'update_time': new_update})
                    else:
                        print("New story found! Making reddit post...")
                        self.post_to_subreddit(sub_info['name'], title, link,
                                               current_feed['flair'] if 'flair' in current_feed else None)
                        new_update = int(time.time()) + current_feed['check_interval']
                        sources[url]['last_id'] = guid
                        update_entry.update({'update_time': new_update,
                                             'update_index': (update_entry['update_index'] + 1) % len(
                                                 current_feed['urls']), 'listening': False})
                    next_update = min(new_update, next_update)
                # Update time has not passed
                else:
                    next_update = min(update_entry['update_time'], next_update)
        return next_update

    def post_to_subreddit(self, sub_name, title, link, flair_text=None):
        def post_with_flair():
            # Find flair_id
            flair_choices = list(subreddit.flair.link_templates.user_selectable())
            for flair in flair_choices:
                if flair["flair_text"] == flair_text:
                    if not self.testing:
                        subreddit.submit(title=title, url=link, resubmit=False, flair_id=flair["flair_template_id"])
                    send_discord_message(f"Posted {link} to r/{sub_name}")
                    print(f"Posted to {sub_name} with preset flair {flair_text}")
                    return
            # Use editable flair if no pre-defined flair found
            for flair in flair_choices:
                if flair['flair_text_editable']:
                    if not self.testing:
                        subreddit.submit(title=title, url=link, resubmit=False, flair_id=flair["flair_template_id"],
                                         flair_text=flair_text)
                    send_discord_message(f"Posted {link} to r/{sub_name}")
                    print(f"Posted to {sub_name} with custom flair {flair_text}")
                    return
            # Use default flair if no editable flair found
            if not self.testing:
                subreddit.submit(title=title, url=link, resubmit=False)
            send_discord_message(f"Posted {link} to r/{sub_name}")
            print(f"Posted to {sub_name}, flair_text not found")

        def post_without_flair():
            if not self.testing:
                subreddit.submit(title=title, url=link, resubmit=False)
            send_discord_message(f"Posted {link} to r/{sub_name}")
            print(f"Posted to {sub_name}")

        # Posts to subreddit
        try:
            subreddit = self.reddit.subreddit(sub_name)
            if flair_text:
                post_with_flair()
            else:
                post_without_flair()
        except Exception as e:
            print(f'Error posting to {sub_name}: {str(e)}')

    # Main Program Loop
    def run(self):
        while True:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M')}] Checking RSS feeds...")
            next_update = self.subreddits_loop()
            # Update db.json
            if not self.testing:
                print("Updating db.json...")
                update_db('db/db.json', self.db)
            # Wait until next update
            t = datetime.fromtimestamp(next_update).strftime('%Y-%m-%d %H:%M')
            print(f"Next update at {t}")
            until(next_update)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--testing", help="Testing mode toggle", action="store_true")
    bot = RedditBot(parser.parse_args().testing)
    bot.run()
