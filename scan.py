#!/usr/bin/python

import sys, getopt, requests, os, time, smtplib
# Run `pip3 install python-dotenv`
from dotenv import load_dotenv
from email.message import EmailMessage

def printSyntax():
	print('usage: python3 scan.py -u <reddit_username> -p <reddit_password> -s <subreddit_name> -t <text> -e <email>')

def main(argv):
	### VALIDATE ARGUMENTS ###
	username = ''
	password = ''
	subreddit = ''
	text = ''
	email = ''
	if len(sys.argv) != 11:
		print('Invalid number of arguments! Expected arguments: 11. Actual arguments: ', len(sys.argv))
		printSyntax()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv,"u:p:s:t:e:",["username=","password=","subreddit=","text=","email="])
	except getopt.GetoptError:
		print("Unexpected argument.")
		printSyntax()
		sys.exit()
	
	for opt, arg in opts:
		if opt != '-u' and opt != '-p' and opt != '-s' and opt != '-t' and opt != '-e':
			printSyntax()
			sys.exit()
		elif opt in ("-u", "--username"):
			username = arg
		elif opt in ("-p", "--password"):
			password = arg
		elif opt in ("-s", "--subreddit"):
			subreddit = arg
		elif opt in ("-t", "--text"):
			text = arg
		elif opt in ("-e", "--email"):
			email = arg

	url = 'https://oauth.reddit.com/r/' + subreddit + '/new.json?limit=20'

	### Set up reddit API authentication ###
	load_dotenv()
	CLIENT_ID = os.getenv("CLIENT_ID")
	SECRET_TOKEN = os.getenv("SECRET_TOKEN")
	auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN) 
	data = {'grant_type': 'password','username': username,'password': password}
	headers = {'User-Agent': 'scanner/0.0.1'}
	isMatch = False;	

	### MAIN LOOP ###
	while not isMatch:
		res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
		TOKEN = res.json()['access_token']
		headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

		requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
		res = requests.get(url, headers=headers)

		### JSON PARSER ###	
		for post in res.json()['data']['children']:
			if text.lower() in post['data']['title'].lower():
				### SEND EMAIL ###
				isMatch = True;
				msg = EmailMessage()
				msg['Subject'] = "Match found for text: " + text.lower() + " in subreddit: " + subreddit
				msg['From'] = "subredditscanner@gmail.com"
				msg['To'] = email
				msg.set_content(post['data']['url'])

				smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
				smtp.login("subredditscanner@gmail.com", os.getenv("EMAIL_PASSWD")) 
				smtp.send_message(msg)
				smtp.close()
				break

		if not isMatch:
			time.sleep(300)
	### END LOOP ###

if __name__ == "__main__":
	main(sys.argv[1:])
