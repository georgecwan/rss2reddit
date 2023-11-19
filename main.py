import argparse
import os
from rss_script import RedditBot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--testing", help="Testing mode toggle", action="store_true")
    bot = RedditBot(parser.parse_args().testing, os.path.abspath("config.yaml"), os.path.abspath("db/db.json"),
                    os.path.abspath("db/rss_script.log"))
    bot.run()
