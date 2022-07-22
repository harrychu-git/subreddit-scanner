#!/usr/bin/python

import sys, getopt, requests, os, time
# Run `pip3 install python-dotenv`
from dotenv import load_dotenv

def printSyntax():
	print('usage: python3 scan.py -u <reddit_username> -p <reddit_password> -s <subreddit_name> -t <text>')

def main(argv):
	### VALIDATE ARGUMENTS ###
	username = ''
	password = ''
	subreddit = ''
	text = ''
	if len(sys.argv) != 9:
		print('Invalid number of arguments! Expected arguments: 9. Actual arguments: ', len(sys.argv))
		printSyntax()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv,"u:p:s:t:",["username=","password=","subreddit=","text="])
	except getopt.GetoptError:
		print("Unexpected argument.")
		printSyntax()
		sys.exit()
	
	for opt, arg in opts:
		if opt != '-u' and opt != '-p' and opt != '-s' and opt != '-t':
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

	url = 'https://oauth.reddit.com/r/' + subreddit + '/new.json?limit=20'
	print('Username is: ', username)
	print('URL is: ', url)
	print('Text is: ', text)

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
			print(post['data']['title'])
			if text.lower() in post['data']['title'].lower():
				isMatch = True;
				print("Match found: ", text.lower(), " (Implement some notifier)")
		if not isMatch:
			time.sleep(300)
	### END LOOP ###

if __name__ == "__main__":
	main(sys.argv[1:])
