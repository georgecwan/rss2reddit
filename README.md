# RSS2Reddit

![GitHub release (latest by date)](https://img.shields.io/github/v/release/GcWan/rss2reddit?sort=semver)
![MIT License](https://img.shields.io/github/license/GcWan/rss2reddit)

### Description

This script will post the latest news (title and link) from RSS feeds to subreddits of your choice. Each subreddit can
be configured with multiple lists of RSS feeds. The script will go through each feed in each list and listen to them
one at a time. While listening, the script will check the RSS feed for new items every 30 minutes. If a new item is
found, the script will post the new item's url address in the corresponding subreddit. *(Note: only links added to the
RSS feed **after** the script begins listening will be posted)* After posting, the script will not check the RSS feed
for new links and any updates to the RSS feed will be ignored until the script begins listening to the RSS feed again.
To better understand the functionalities of this script, please read
the [Config Documentation](https://github.com/GcWan/rss-to-subreddit/wiki/V2-Config-Documentation)
in the wiki.

Note: You should only use this on subreddits that you moderate. Make sure you do not break Reddit's terms of service or
subreddit rules while using this script.

## Table of Contents

- [Setup Steps](#setup-steps)
    - [Register app on Reddit](#register-app-on-reddit)
    - [Setting up Config.yaml](#setting-up-configyaml)
- [Running the Script](#running-the-script)
    - [Option 1: Local Python Installation](#option-1-local-python-installation)
    - [Option 2: Docker Compose](#option-2-docker-compose)
- [Setting up a Discord Webhook](#setting-up-a-discord-webhook)
- [Useful Links](#useful-links)

## Setup Steps

Download the desired [release of this repository](https://github.com/GcWan/rss2reddit/releases) and unzip it on
your own computer. This README is only applicable for release v2.0.0. If you would like to use a different version,
please find the corresponding usage instructions inside the [wiki](https://github.com/GcWan/rss2reddit/wiki).

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

### Setting Up Config.yaml

#### Config.yaml Format

```yaml
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
    - Do not add duplicate entries with the same pairing of subreddit and RSS url.
    - Although most strings do not have to be surrounded by quotes, your RSS url might have to be surrounded by quotes
      if it contains special characters.
- The delay parameter should be a positive integer representing how many seconds the program waits before
  listening to RSS feed for updates.
    - The flair parameter is optional. If you want to add a flair to your posts, enter the text you want to use as
      flair.
      Otherwise, do not include the flair parameter in your config file.
- Make sure that the config.yaml file is indented correctly. The indentation should be 2 spaces for each level.
  The program will not be able to read the config file if the indentation is incorrect.

**KEEP THE CREDENTIALS IN CONFIG.YAML PRIVATE. DO NOT SHARE WITH ANYONE ELSE.**

## Running the Script

You can run the script using either a Python 3 environment or a Docker container.

### Option 1: Local Python Installation

#### Step 1: Install Python dependencies

This step only needs to be completed **_once_** after download. If you have completed this step before, skip
to [Step 2](#step-2-start-the-script).

- Install Python 3.8 or higher [here](https://www.python.org/downloads/)
    - Select the option to add Python to path during installation if it appears
    - If you have a preexisting installation of Python 3.8 or higher, you do not have to reinstall it.
- Open your command-line app (e.g. Powershell, Terminal, etc.)
- Type `python --version` and press enter. Make sure that the Python version shown is 3.8 or higher. You may need to
  download a newer version of Python otherwise.
    - If the Python version is shown to be Python 2, you may have to run the same command with `python3` instead
      of `python` (e.g. `python3 --version`). If the correct command `python3`, Make sure to use the `python3` command
      for all the steps below as well.
- Navigate to your local copy of the rss2reddit folder: `cd PATH_TO_FOLDER`
    - If you are unsure about the path, dragging the folder into the command line interface might paste the path in for
      you. On some platforms, you can also right-click the folder and select "Copy as path".
- **Optional but recommended:** Create a virtual environment: `python -m venv venv`
    - Activate the virtual environment: `venv\Scripts\activate.bat` (Windows CMD) or `source venv/bin/activate` (
      Mac/Linux)
    - It should say (venv) at the beginning of the command line prompt if the virtual environment is active.
    - If you encounter errors trying to create the virtual environment, you can find links to helpful tutorials in
      the [Useful Links](#useful-links) section.
- Install dependencies from requirements.txt: `python -m pip install -r requirements.txt`

#### Step 2: Start the script

- If you haven't already, navigate to your local copy of the rss2reddit folder: `cd PATH_TO_FOLDER`
- If you created a virtual environment, activate it: `venv\Scripts\activate.bat` (Windows CMD)
  or `source venv/bin/activate` (
  Mac/Linux)
- Run script: `python main.py` or `python3 main.py`
    - You should start to see output in the command line interface indicating that the script is running.
    - Note that you might terminate the script if you close the command line interface. If you want to keep the script
      running in the background, you will have to find external resources on how to do so.
- Stop the script with Ctrl-C
- If you created a virtual environment, you can deactivate it with `deactivate`
- Note that the script has to be restarted to reflect any changes made inside the folder, including changes to
  config.yaml.

### Option 2: Docker Compose

#### Step 1: Installing Docker

This step only needs to be completed **_once_** after download. If you have completed this step before, skip
to [Step 2](#step-2-start-the-docker-container).

- Install Docker [here](https://docs.docker.com/get-docker/)
- *Optional:* When you run the Docker container, it will use UTC time by default. If you want the program to
  display your own timezone, follow the steps below:
    - Look up your timezone's TZ database name
      [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
    - Open docker-compose.yaml in a text editor of your choice
    - Enter your own timezone's TZ database name after the `TZ=`
    - E.g. `- TZ=America/New_York`

#### Step 2: Start the Docker Container

- Open your command-line app (e.g. Powershell, Terminal, etc.)
- Navigate to your local copy of the rss2reddit folder: `cd PATH_TO_FOLDER`
    - If you are unsure about the path, dragging the folder into the command line interface might paste the path in for
      you. On some platforms, you can also right-click the folder and select "Copy as path".
- Run the Docker container using Docker Compose: `docker compose up -d`
    - If you have made changes to files within the folder including config.yaml since the last time you built the Docker
      image, you will have to
      run `docker compose up -d --build` to rebuild the image. Otherwise, the script will use the old config file.
- If you wish to see the output of the script, run `docker logs -f rss-script` or use Docker
  Desktop. If you press Ctrl-C while viewing the output, the output will stop being displayed but the script will
  continue to run in the background.
- To stop the Docker container: `docker compose down` or use Docker Desktop. Note that closing the command line
  interface or Docker Desktop alone will not stop the script.
- Note: You may have to adjust the CPU and memory constraints in Docker Desktop if the script is using too much of your
  computer's resources. The script should not use more than half a CPU core and 100MB of memory.

## Setting up a Discord Webhook

If you would like to receive notifications about new posts in a Discord server, you can set up a Discord webhook.
These steps are completely optional and the script will still work without a Discord webhook.

### Create a Webhook in Discord

- Go to the server settings of your Discord server
- Find the "Integrations" section and click "Webhooks"
- Click "Create Webhook"
- Give the webhook a name and assign it to the channel you would like to receive notifications in
- Copy the webhook URL
- If you are using a local Python installation, finish up by following the steps
  to [create a .env file](#creating-a-env-file-local-python-installation-or-docker).
- If you are using Docker, you can either [create a .env file](#creating-a-env-file-local-python-installation-or-docker)
  or [set environment variables in docker-compose.yaml](#setting-environment-variables-in-docker-composeyaml-docker-only).
  You do _not_ need to do both.

### Creating a .env file (local Python installation or Docker)

- Create a file named ".env" in your local copy of the rss2reddit folder
    - You can do this by running `touch .env` in Terminal (Mac/Linux) or by creating a new file using Notepad on Windows
- Enter `DISCORD_WEBHOOK_URL=` followed by the webhook URL you copied from Discord and save the file
- Redo the steps from [starting the script](#step-2-start-the-script). When the script starts running, you should
  receive a notification in the Discord channel you specified.

### Setting environment variables in docker-compose.yaml (Docker only)

- Open docker-compose.yaml in a text editor of your choice
- Delete the `#` symbol to uncomment the line `DISCORD_WEBHOOK_URL=`
- Paste the webhook URL you copied from Discord after the `=`
- Redo the steps from [starting the Docker container](#step-2-start-the-docker-container). After the container restarts,
  you should receive a notification in the Discord channel you specified.

# Useful Links

- [Reddit Help](https://www.reddithelp.com/hc/en-us)
- [Reddit Bottiquette](https://www.reddit.com/wiki/bottiquette/)
- [Python Virtual Environments Primer](https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
