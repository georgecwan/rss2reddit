from datetime import datetime
import argparse
import math
import praw
import requests
import time
from pprint import pprint

from file_manager import load_config, load_db, update_db
from rss_parser import find_newest_headline
from notif import send_discord_notification
from pause import until


class RedditBot:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"

    def __init__(self, testing):
        # Sets testing mode
        self.testing = testing
        print(f"Testing Mode: {'ON' if self.testing else 'OFF'}")
        # Initializes db dictionary, sets self.db
        self.db = load_db('db/db.json')
        # Loads config file, sets self.credentials and self.sub_list
        self.credentials, self.sub_list = load_config('config.yaml')
        print("Config List:", end=' ')
        pprint(self.sub_list)
        # Initializes reddit praw object
        self.reddit = praw.Reddit(username=self.credentials['user'],
                                  password=self.credentials['password'],
                                  client_id=self.credentials['client_id'],
                                  client_secret=self.credentials['client_secret'],
                                  user_agent="Subreddit-News:V1.0 by /u/GeoWa")
        # Sends Discord Notification
        send_discord_notification(f"Bot Started on {'Testing Mode' if self.testing else 'Normal Mode'}")

    def rss_request(self, url, key):
        try:
            resp = requests.get(url, headers={
                'User-Agent': self.USER_AGENT,
                'If-Modified-Since': self.db[key]["Last_Modified"],
                'If-None-Match': self.db[key]["ETag"]
            })
            if resp.status_code == 200:
                self.db[key]["Last_Modified"] = resp.headers[
                    'Last-Modified'] if 'Last-Modified' in resp.headers else None
                self.db[key]["ETag"] = resp.headers['ETag'] if 'ETag' in resp.headers else None
                return resp.text
            else:
                return None
        except Exception as e:
            print(f'Error requesting {url}: {str(e)}')

    def subreddits_loop(self):
        next_update = math.inf  # next_update is the time in seconds until the next update
        for sub_info in self.sub_list:
            print(f"Checking r/{sub_info['subreddit_name']} with {sub_info['rss_url']}...")
            key = sub_info['subreddit_name'] + sub_info['rss_url']
            # New entry
            if key not in self.db:
                self.db[key] = {'Last_Modified': None, 'ETag': None, 'Listening': True}
                print(f"Listening to {sub_info['rss_url']} for r/{sub_info['subreddit_name']}...")
                response_text = self.rss_request(sub_info['rss_url'], key)
                if response_text:
                    new_update = math.ceil(time.time()) + 1800  # Check 30 minutes later
                    self.db[key].update({'Last_Id': find_newest_headline(response_text)[2], 'Update_Time': new_update})
                    next_update = min(new_update, next_update)
            # Update time has passed
            elif self.db[key]['Update_Time'] <= math.ceil(time.time()):
                response_text = self.rss_request(sub_info['rss_url'], key)
                if not response_text:
                    print("No new data from RSS feed, continuing to listen")
                    new_update = int(time.time()) + 1800  # Check 30 minutes later
                    next_update = min(new_update, next_update)
                    self.db[key].update({'Update_Time': new_update, 'Listening': True})
                    continue
                title, link, guid = find_newest_headline(response_text)
                # Check for errors from RSSParser.py
                if not title:
                    continue
                if self.db[key]['Last_Id'] == guid:
                    print("No new stories since last check, continuing to listen")
                    new_update = int(time.time()) + 1800  # Check 30 minutes later
                    self.db[key].update({'Update_Time': new_update, 'Listening': True})
                elif self.db[key]['Listening']:
                    print("New story found! Making reddit post...")
                    self.post_to_subreddit(sub_info['subreddit_name'], title, link,
                                           sub_info['flair'] if 'flair' in sub_info else None)
                    new_update = int(time.time()) + sub_info['delay']
                    self.db[key].update({'Last_Id': guid, 'Update_Time': new_update, 'Listening': False})
                else:  # Not Listening
                    print(f"Began listening")
                    new_update = int(time.time()) + 1800  # Check 30 minutes later
                    self.db[key].update({'Last_Id': guid, 'Update_Time': new_update, 'Listening': True})
                next_update = min(new_update, next_update)
            # Update time has not passed
            else:
                next_update = min(self.db[key]['Update_Time'], next_update)
        return next_update

    def post_to_subreddit(self, sub_name, title, link, flair_text=None):
        def post_with_flair():
            # Find flair_id
            flair_choices = list(subreddit.flair.link_templates.user_selectable())
            for flair in flair_choices:
                if flair["flair_text"] == flair_text:
                    if not self.testing:
                        subreddit.submit(title=title, url=link, resubmit=False,
                                         flair_id=flair["flair_template_id"])
                    send_discord_notification(f"Posted {link} to r/{sub_name}")
                    print(f"Posted to {sub_name} with preset flair {flair_text}")
                    return
            # Use editable flair if no pre-defined flair found
            for flair in flair_choices:
                if flair['flair_text_editable']:
                    if not self.testing:
                        subreddit.submit(title=title, url=link, resubmit=False,
                                         flair_id=flair["flair_template_id"], flair_text=flair_text)
                    send_discord_notification(f"Posted {link} to r/{sub_name}")
                    print(f"Posted to {sub_name} with custom flair {flair_text}")
                    return
            # Use default flair if no editable flair found
            if not self.testing:
                subreddit.submit(title=title, url=link, resubmit=False)
            send_discord_notification(f"Posted {link} to r/{sub_name}")
            print(f"Posted to {sub_name}, flair_text not found")

        def post_without_flair():
            if not self.testing:
                subreddit.submit(title=title, url=link, resubmit=False)
            send_discord_notification(f"Posted {link} to r/{sub_name}")
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
