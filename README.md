# subreddit-scanner

## Description

This python script will search the 20 newest posts in a subreddit for a text string every 5 minutes. If a match is found, it will send an email to you to notify you of a match. At this point, the script will exit out. The intended use-case is to track deals on subreddits such as "buildapcsales", "gamedeals", "frugalmalefashion", etc...

## Prerequisites

You will need an existing reddit account and a destination email address.

Install [Python](https://www.python.org/downloads/) version 3.6 or newer.

Install the Python dotenv library.

`pip3 install python-dotenv`

## Instructions

Fork this repository or simply copy the python script to your local repository.

Create a `.env` file in the same working directory.

Add the following lines to `.env`:

```
CLIENT_ID = '<reddit_app_client_id>'
SECRET_TOKEN = '<reddit_app_secret_token>'
EMAIL_PASSWD = '<gmail_account_app_password>'
```
You can request these values from the script's maintainer. Alternatively, you can create your own reddit application and gmail account. Refer to the below two links for implementation tips.

* https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
* https://pythoninoffice.com/send-gmail-using-python/

Usage: `python3 scan.py -u <reddit_username> -p <reddit_password> -s <subreddit_name> -t <text> -e <email>`

## Environment

Tested on Python 3.6.9
