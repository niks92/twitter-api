import json
import logging
import unicodecsv as csv
from twython import TwythonStreamer
import pandas as pd


def load_credentials():
	"""Load credentials from json file"""

	with open("./twitter_credentials.json", "r") as file:
		return json.load(file)

if __name__ == '__main__':
	
	from twython import Twython
	try:
		count=1
		max_id=''
		creds = load_credentials()
		twitter = Twython(creds['credentials']['CONSUMER_KEY'], creds['credentials']['CONSUMER_SECRET'], creds['credentials']['ACCESS_TOKEN'],
			creds['credentials']['ACCESS_SECRET'])
		api_url = 'https://api.twitter.com/1.1/search/tweets.json'
		final=[]
		results = twitter.cursor(twitter.search, q='Narendra Modi',
			tweet_mode='extended', lang='en', count=100, max_id=max_id)
		for result in results:
			tweet=dict()
			tweet['id'] = result['id']

			try:
				tweet['full_text'] = str(result['full_text'].encode('utf8'))
			except KeyError as e:
				tweet['full_text'] = str(result['text'].encode('utf8'))
			tweet['location'] = result['user']['location']

			try:
				tweet['hashtags'] = result['entities']['hashtags'][0]['text']
			except Exception as ee:
				tweet['hashtags'] = ""

			tweet['created_at'] = result['created_at']
			tweet['lang'] = result['lang']
			tweet['is_retweeted'] = result['retweeted']
			tweet['user'] = result['user']['id']
			max_id=result['id']
			count=count+1
			# change the count for how many datasets you want to change
			if count==10000:
				break
			print(count)
			final.append(tweet)
		#ADD to csv
		toCSV = final
		keys = toCSV[0].keys()
		with open('saved_tweets.csv', 'wb') as output_file:
			dict_writer = csv.DictWriter(output_file, keys)
			dict_writer.writeheader()
			dict_writer.writerows(toCSV)
	except Exception as e:
		print(e)

