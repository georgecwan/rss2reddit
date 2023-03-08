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
            "delay": "delay_in_seconds",
            "flair": "flair_text"
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
  checking the RSS feed for updates. This is the only paramater that does not have quotation marks around it.
  - The flair parameter is optional. If you want to add flair to your posts, enter the text you want to use as flair.
  Otherwise, do not include the flair parameter in your config file. 
    - Format for one subreddit (no flairs):
      ```
        "subreddits": [
            {
                "subreddit_name": "NAME_OF_SUB_TO_POST_TO",
                "rss_url": "URL_OF_RSS_FEED",
                "delay": ENTER_NUMBER
            }
        ]
        ```
      - Format for three subreddits (some flairs):
        ```
          "subreddits": [
              {
                  "subreddit_name": "NAME_OF_SUB_TO_POST_TO",
                  "rss_url": "URL_OF_RSS_FEED",
                  "delay": ENTER_NUMBER,
                  "flair": "FLAIR_TEXT"
              },
              {
                  "subreddit_name": "SECOND_SUB",
                  "rss_url": "SECOND_URL",
                  "delay": ENTER_NUMBER
              },
              {
                  "subreddit_name": "THIRD_SUB",
                  "rss_url": "THIRD_URL",
                  "delay": ENTER_NUMBER,
                  "flair": "FLAIR_TEXT"
              }
          ]
          ```
- Everything in the config file except the delay values should be contained in quotes.

**KEEP YOUR OWN CONFIG.JSON PRIVATE. DO NOT SHARE WITH ANYONE ELSE.**

# Running the Script
- Install Python [here](https://www.python.org/downloads/)
  - Select the option to add Python to path during installation if it appears
  - If Python 3 is already installed on your machine, you do not have to reinstall it
- Open your command-line app (e.g. Powershell, Terminal, etc.)
- Type `python --version` and press enter. Make sure that the Python version shown is 3.10 or later, you may need to download a newer version of Python otherwise.
  - If the Python version is shown to be Python 2, you may have to run the same command with `python3` instead of `python` (e.g. `python3 --version`). If that is the case, make sure to use the `python3` commmand for all the steps below as well.
- Navigate to your local copy of the RSS-to-Subreddit folder: `cd PATH_TO_FOLDER`
  - If you are unsure about the path, dragging the folder into the command line interface will paste the path in for you.
- **Optional but recommended:** Create a virtual environment: `python -m venv venv`
  - Activate the virtual environment: `venv\Scripts\activate.bat` (Windows CMD) or `source venv/bin/activate` (Mac/Linux)
  - It should say (venv) at the beginning of the command line prompt if the virtual environment is active.
  - If you encounter errors trying to create the virtual environment, you can find links to helpful tutorials in the [Useful Links](#useful-links) section.
- Install dependencies from requirements.txt: `python -m pip install -r requirements.txt`
- Run script: `python main.py`
- Exit the script with Ctrl-C (Note: Reddit posts will stop being made by the script if you end it)
- If you created a virtual environment, you can deactivate it with `deactivate`

# Useful Links
- [Reddit Help](https://www.reddithelp.com/hc/en-us)
- [Reddit Bottiquette](https://www.reddit.com/wiki/bottiquette/)
- [Python Virtual Environments Primer](https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment)
