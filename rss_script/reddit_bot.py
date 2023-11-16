from datetime import datetime, timedelta
import math
import time
import sys

import praw
import requests
from pprint import pprint

from . import utils


class RedditBot:
    """
    RedditBot class that handles all the Reddit API calls and RSS requests

    Attributes
    ----------
    testing : bool
        Boolean to determine if the bot is in testing mode. If True, the bot will not post to Reddit or update the
        db.json file.
    credentials : dict
        Dictionary containing the credentials for the Reddit API
    sub_list : list
        List of dictionaries containing the subreddits' information. Each dictionary contains 'name', the subreddit's
        name, and 'rss_feeds', the list of RSS feeds to check. Each item in 'rss_feeds' contains 'urls', the list of RSS
        urls to check, 'check_interval', the time in seconds between each check, and optionally 'flair', the flair to
        use when making Reddit posts of the RSS feed.
    db_file : str
        The absolute path to the database file
    db : dict
        Dictionary containing the database. This dictionary is loaded from and stored into the db_file
    reddit : Reddit object
        Reddit object from praw used to interact with the Reddit API
    USER_AGENT : str
        String used to identify the browser when making requests to the RSS feeds
    """

    USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36")

    def __init__(self, testing: bool, config_file: str, db_file: str) -> None:
        """
        Initializes the RedditBot object

        Args:
            testing: Boolean to determine if the bot is in testing mode. If True, the bot will not post to Reddit or
                update the db.json file.
            config_file: The absolute path to the config file
            db_file: The absolute path to the database file

        Returns:
            None
        """
        # Sets testing mode
        self.testing = testing
        print(f"Testing Mode: {'ON' if self.testing else 'OFF'}")
        # Loads config file, sets self.credentials and self.sub_list
        self.sub_list, self.credentials = utils.load_config(config_file)
        print("Config List:")
        pprint(self.sub_list)
        print("")
        # Initializes db dictionary, sets self.db
        self.db_file = db_file
        self.db = utils.load_db(db_file)
        self._initialize_db()
        # Initializes reddit praw object
        self.reddit = praw.Reddit(username=self.credentials['user'], password=self.credentials['password'],
                                  client_id=self.credentials['client_id'],
                                  client_secret=self.credentials['client_secret'],
                                  user_agent="Subreddit-News:V1.0 by /u/GeoWa")
        # Sends Discord Notification
        utils.send_discord_message(
            f"Bot Started on {'Testing Mode' if self.testing else 'Normal Mode'} at {time.strftime('%Y-%m-%d %H:%M')}")

    def _initialize_db(self) -> None:
        """
        Initializes the database by adding any new subreddits and RSS feeds to the database

        Precondition:
            self.db is initialized with values from db.json
        Returns:
            None
        """
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

    def run(self) -> None:
        """
        Main program loop that checks the RSS feeds, updates the db.json file, then sleeps for a specified amount of
        time.
        """
        while True:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M')}] Checking RSS feeds...")
            next_update = self._subreddits_loop()
            # Update db.json
            if not self.testing:
                print("Updating db.json...")
                utils.update_db(self.db_file, self.db)
            # Wait until next update
            t = datetime.fromtimestamp(next_update).strftime('%Y-%m-%d %H:%M')
            print(f"Next update at {t}")
            utils.until(next_update)

    def _subreddits_loop(self) -> float:
        """
        Loops through all the subreddits and RSS feeds and checks for new entries

        Returns:
            The time in seconds until the next time the loop should run
        """
        next_update = math.inf  # next_update is the time in seconds until the next update
        for sub_info in self.sub_list:
            print(f"Checking r/{sub_info['name']}...")
            updates = self.db[sub_info['name']]['update_list']
            sources = self.db[sub_info['name']]['rss_sources']
            for index in range(len(sub_info['rss_feeds'])):
                current_feed = sub_info['rss_feeds'][index]
                update_entry = updates[index]
                url = current_feed['urls'][update_entry['update_index']]
                # Update time has passed
                if update_entry['update_time'] <= math.ceil(time.time()):
                    next_update = min(self._handle_update(sub_info, sources, current_feed, update_entry, url),
                                      next_update)
                # Update time has not passed
                else:
                    next_update = min(update_entry['update_time'], next_update)
        return next_update

    def _handle_update(self, sub_info: dict, sources: dict, current_feed: dict, update_entry: dict, url: str) -> float:
        """
        Updates a specific subreddit-RSS feed combination by making a request to the RSS feed, updating the db, and
        posting to Reddit if applicable.

        Args:
            sub_info: Config dictionary for the subreddit
            sources: DB entry containing list of URL and update about the RSS feeds to check for the subreddit
            current_feed: DB entry containing a group of RSS feeds to check and the update interval
            update_entry: DB entry containing the update time, update index, and listening mode for the RSS feed group
            url: The url of the RSS feed

        Returns:
            Timestamp of when this subreddit-RSS feed combination should next enter listening mode.
        """
        # New Entry
        if url not in sources:
            sources[url] = {'last_modified': None, 'etag': None, 'last_id': None}
            print(f"Adding {url} to db...")
        # Get RSS Feed
        response_text = self._rss_request(url, sub_info['name'])
        if not response_text:
            print(f"No new data from {url}, continuing to listen")
            new_update = int(time.time()) + 1800  # Check 30 minutes later
            update_entry.update({'update_time': new_update, 'listening': True})
            return new_update
        title, link, guid = utils.find_newest_headline(response_text)
        # Check for errors from RSSParser.py
        if not title:
            return math.inf
        return self._handle_rss_response(sub_info, sources, current_feed, update_entry, url, title,
                                         link, guid)

    def _rss_request(self, url: str, subreddit: str) -> str | None:
        """
        Makes a request to the RSS feed and returns the response text if the request is successful

        Args:
            url: The url of the RSS feed
            subreddit: The name of the subreddit with the RSS entry

        Returns:
            The response text of the RSS feed if the request is successful, None otherwise
        """
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
            return None

    def _handle_rss_response(self, sub_info: dict, sources: dict, current_feed: dict, update_entry: dict, url: str,
                             title: str, link: str, guid: str) -> int:
        """
        Handles the response from the RSS feed by updating the db, managing the listening mode, and posting to Reddit if
        applicable.

        Args:
            sub_info: Config dictionary for the subreddit
            sources: DB entry containing list of URL and update about the RSS feeds to check for the subreddit
            current_feed: DB entry containing a group of RSS feeds to check and the update interval
            update_entry: DB entry containing the update time, update index, and listening mode for the RSS feed group
            url: The url of the RSS feed
            title: Title of the latest article from the RSS feed
            link: Link to the latest article from the RSS feed
            guid: GUID of the latest article from the RSS feed

        Returns:

        """
        # Update db and post to Reddit
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
            print("New story found! Checking for duplicates...")
            if self._check_for_duplicates(title, link, self.reddit.subreddit(sub_info['name'])):
                new_update = int(time.time()) + 1800  # Check 30 minutes later
                sources[url]['last_id'] = guid
                update_entry.update({'update_time': new_update, 'listening': True})
            else:
                print("No duplicates found, posting to Reddit...")
                self._post_to_subreddit(sub_info['name'], title, link,
                                        current_feed['flair'] if 'flair' in current_feed else None)
                new_update = int(time.time()) + current_feed['check_interval']
                sources[url]['last_id'] = guid
                update_entry.update({'update_time': new_update,
                                     'update_index': (update_entry['update_index'] + 1) % len(current_feed['urls']),
                                     'listening': False})
        return new_update

    @staticmethod
    def _check_for_duplicates(title: str, link: str, subreddit: praw.reddit.Subreddit) -> bool:
        """
        Checks if the post is a duplicate by comparing the title and link to posts in the subreddit
        from the last 24 hours (up to 1000 posts).
        Links are checked for exact matches, titles are checked for similarity using a spaCy model.
        The current threshold for similarity is 0.8.

        Args:
            title: The title of the post
            link: The url link of the post
            subreddit: The name of the subreddit to check for duplicate posts in

        Returns:
            True if the post is a duplicate, False otherwise
        """
        try:
            # Calculate the timestamp for the past 6 hours
            past_timestamp = int((datetime.now() - timedelta(hours=24)).timestamp())
            for post in subreddit.new(limit=1000):
                if post.created_utc < past_timestamp:
                    return False
                if utils.remove_query_params(link) == post.url or link == post.url:
                    utils.send_discord_message(f"Duplicate found: https://www.reddit.com{post.permalink}")
                    print(f"Duplicate found: https://www.reddit.com{post.permalink}")
                    return True
                similarity = utils.get_similarity(title, post.title)
                # Only here for testing, remove later
                if similarity > 0.8:
                    utils.send_discord_message(
                        f"Similar title found with a similarity of {similarity}: \n- {title} \n- {post.title}\n"
                        f"Source: https://www.reddit.com{post.permalink}")
                    print(f"Similar title found: {title} and {post.title} with a similarity of {similarity}")
                    return True
                elif similarity > 0.75:
                    utils.send_discord_message(
                        f"Still posting with a similarity of {similarity}: \n- {title} \n- {post.title}\n"
                        f"Source: https://www.reddit.com{post.permalink}")
        except Exception as e:
            print(f'Error checking for duplicates: {str(e)}')
            return False

    def _post_to_subreddit(self, sub_name: str, title: str, link: str, flair_text: str | None = None) -> None:
        """
        Posts to the subreddit with the given flair_text if applicable

        Args:
            sub_name: The name of the subreddit to post to
            title: The title of the post
            link: The url link of the post
            flair_text: (Optional) The flair text to use for the post
        """

        def post_with_flair() -> None:
            """Posts to the subreddit with the given flair_text"""
            # Find flair_id
            flair_choices = list(subreddit.flair.link_templates.user_selectable())
            for flair in flair_choices:
                if flair["flair_text"] == flair_text:
                    if not self.testing:
                        subreddit.submit(title=title, url=link, resubmit=False, flair_id=flair["flair_template_id"])
                    utils.send_discord_message(f"Posted {link} to r/{sub_name}")
                    print(f"Posted to {sub_name} with preset flair {flair_text}")
                    return
            # Use editable flair if no pre-defined flair found
            for flair in flair_choices:
                if flair['flair_text_editable']:
                    if not self.testing:
                        subreddit.submit(title=title, url=link, resubmit=False, flair_id=flair["flair_template_id"],
                                         flair_text=flair_text)
                    utils.send_discord_message(f"Posted {link} to r/{sub_name}")
                    print(f"Posted to {sub_name} with custom flair {flair_text}")
                    return
            # Use default flair if no editable flair found
            if not self.testing:
                subreddit.submit(title=title, url=link, resubmit=False)
            utils.send_discord_message(f"Posted {link} to r/{sub_name}")
            print(f"Posted to {sub_name}, flair_text not found")

        def post_without_flair() -> None:
            """Posts to the subreddit without a flair"""
            if not self.testing:
                subreddit.submit(title=title, url=link, resubmit=False)
            utils.send_discord_message(f"Posted {link} to r/{sub_name}")
            print(f"Posted to {sub_name}")

        # Posts to subreddit
        try:
            subreddit = self.reddit.subreddit(sub_name)
            if self._check_for_duplicates(title, link, subreddit):
                return
            if flair_text:
                post_with_flair()
            else:
                post_without_flair()
        except Exception as e:
            print(f'Error posting to {sub_name}: {str(e)}')
