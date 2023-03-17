# RSS to Subreddit
### Description
This script will post the latest news (title and link) from RSS feeds to subreddits of your choice. Multiple pairs of
subreddits and RSS feeds can be configured, with each pair independently alternating between listening and sleeping mode.
In listening  mode, the script will check the RSS feed for new links every 30 minutes. If a new link is found,
the script will post the new link to the corresponding subreddit. *(Note: only links added to the RSS feed **after**
the script begins listening will be posted)* In sleeping mode, the script will not check the RSS feed for new links and
any updates to the RSS feed during sleeping mode will be ignored.

Note: You should only use this on subreddits that you moderate.
## Table of Contents
- [Setup Steps](#setup-setup)
  - [Register app on Reddit](#register-app-on-reddit)
  - [Setting up Config.yaml](#updating-configyaml)
- [Running the Script](#running-the-script)
  - [Option 1: Python Virtual Environment](#option-1-python-virtual-environment)
  - [Option 2: Docker Container](#option-2-docker-container)
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
### Updating Config.yaml
#### Config.yaml Format
```
---
# Credentials
user: my_username
password: my_password
client_id: client_id
client_secret: client_secret
---
# Subreddits
- subreddit_name: subreddit_name1
  rss_url: rss_url1
  delay: delay_in_seconds1
  flair: optional_flair1
- subreddit_name: subreddit_name2
  rss_url: rss_url2
  delay: delay_in_seconds2
```
- Open the config.yaml file in a text editor of your choice.
- Fill in the username and password fields with the username and password of your Reddit account.
  - Enter the client id and client secret from the [previous step](#register-app-on-reddit).
- Fill in the "Subreddits" section with a list of all the subreddits and the corresponding
  RSS url to generate posts from.
  - You may add/remove as many subreddits as you want as long as they follow the format in the template above.
- The delay parameter should be a positive integer representing how many seconds the program waits before 
  listening to RSS feed for updates.
  - The flair parameter is optional. If you want to add a flair to your posts, enter the text you want to use as flair.
    Otherwise, do not include the flair parameter in your config file.
- Make sure that the config.yaml file is indented correctly. The indentation should be 2 spaces for each level.
  The program will not be able to read the config file if the indentation is incorrect.

**KEEP YOUR OWN CONFIG.YAML PRIVATE. DO NOT SHARE WITH ANYONE ELSE.**

# Running the Script
You can run the script using either a Python virtual environment or a Docker container.
## Option 1: Python Virtual Environment
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
  - You should start to see ouput in the command line interface indicating that the script is running.
- Exit the script with Ctrl-C (Note: Reddit posts will stop being made by the script if you end it)
- If you created a virtual environment, you can deactivate it with `deactivate`
## Option 2: Docker Container
- Install Docker [here](https://docs.docker.com/get-docker/)
- Open your command-line app (e.g. Powershell, Terminal, etc.)
- Navigate to your local copy of the RSS-to-Subreddit folder: `cd PATH_TO_FOLDER`
  - If you are unsure about the path, dragging the folder into the command line interface will paste the path in for you.
- Build the Docker image: `docker build -t rss-to-subreddit .`
- (Optional) When you run the Docker container, it will use UTC time by default. If you want the program to
  display your own timezone, follow the steps below:
  - Look up your timezone's TZ database name
    [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
  - Open docker-compose.yaml in a text editor of your choice
  - Delete the two `#` symbols to uncomment the lines
  - Replace the TZ_database_name field with your own timezone's TZ database name
  - E.g. `- TZ: America/New_York`
- Run the Docker container using Docker Compose: `docker compose up -d`
- If you wish to see the output of the script, run `docker logs -f rss-to-subreddit` or open the container in Docker Desktop
- To stop the Docker container: `docker compose down`
# Useful Links
- [Reddit Help](https://www.reddithelp.com/hc/en-us)
- [Reddit Bottiquette](https://www.reddit.com/wiki/bottiquette/)
- [Python Virtual Environments Primer](https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
