# RSS to Subreddit
### Description
This script will post the latest news (title and link) from RSS feeds to subreddits of your choice.

Note: You should only use this on subreddits that you moderate.
## Table of Contents
- [Setup Steps](#setup-setup)
  - [Register app on Reddit](#register-app-on-reddit)
  - [Setting up Config.json](#updating-configjson)
- [Running the Script](#running-the-script)
- [Useful Links](#useful-links)

## Setup Steps
Download this repository as a zip file and unzip it on your own computer.
### Register app on Reddit
- You will need your own reddit account.
- Login to reddit and access account settings [here](https://www.reddit.com/prefs/apps/).
- Scroll to bottom and click button to create app. (Click "are you a developer" if necessary.)
- Fill out form as follows:
  - Name: Subreddit-News by /u/GeoWa
  - App type: script
  - Redirect uri: http://localhost
- The remaining fields are optional.
- Click "create app".
- Copy down the client id (found under the text "Personal Use Script"
and client secret (beside the text "secret").
### Updating Config.json
#### Config.json Format
```
{
    "credentials": {
        "user": "your_username",
        "password": "your_password",
        "client_id": "client_id",
        "client_secret": "client_secret"
    },
    "subreddits": [
        {
            "subreddit_name": "subreddit_name",
            "rss_url": "rss_url",
            "delay": "delay_in_seconds"
        },
        {
            "subreddit_name": "subreddit_name2",
            "rss_url": "rss_url2",
            "delay": "delay_in_seconds2"
        },
        ...
    ]
}
```
- Replace "your_username"" with your username and "your_password" with your password.
  - Enter the client id and client secret from the [previous step](#register-app-on-reddit).
- Fill in the "subreddits" section with a list of all the subreddits and the corresponding
RSS url to generate posts from.
  - The delay parameter should be a positive integer representing how many seconds the program waits before 
    checking the RSS feed for updates. This is the only paramater that **_does not have quotes_**.
  - Format for one subreddit:
    ```
      "subreddits": [
          {
              "subreddit_name": "NAME_OF_SUB_TO_POST_TO",
              "rss_url": "URL_OF_RSS_FEED",
              "delay": ENTER_NUMBER
          }
      ]
      ```
  - Format for three subreddits:
    ```
      "subreddits": [
          {
              "subreddit_name": "NAME_OF_SUB_TO_POST_TO",
              "rss_url": "URL_OF_RSS_FEED",
              "delay": ENTER_NUMBER
          },
          {
              "subreddit_name": "SECOND_SUB",
              "rss_url": "SECOND_URL",
              "delay": ENTER_NUMBER
          },
          {
              "subreddit_name": "THIRD_SUB",
              "rss_url": "THIRD_URL",
              "delay": ENTER_NUMBER
          }
      ]
      ```
- Everything in the config file except the delay values should be contained in quotes.

**KEEP YOUR OWN CONFIG.JSON PRIVATE. DO NOT SHARE WITH ANYONE ELSE.**

# Running the Script
- Install Python
- Install dependecies from requirements.txt
- Run main.py script
- Exit the script with Ctrl-C

# Useful Links
- [Reddit Help](https://www.reddithelp.com/hc/en-us)
- [Reddit Bottiquette](https://www.reddit.com/wiki/bottiquette/)
