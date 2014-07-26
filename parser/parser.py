import csv, re, nltk, string, sys, requests, json
from operator import itemgetter
from nltk.corpus import stopwords
from HTMLParser import HTMLParser

path = "tweets.csv"
output_path = "/tmp"
twitter_username = ""
stop_words = stopwords.words('english')
stop_words.append('http')

labels = []
tweets = []
rownum = 0;
mentions = {}
hashtags = {}
words = {}

##regexes
mention_regex = "\@[A-Za-z0-9_]+"
hashtag_regex = "\#[A-Za-z0-9_]+"
word_regex = "[A-Za-z][A-Za-z0-9_-]+"

print "\n"

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self,d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def get_replies(html):
	replies = []
	html = string.replace(html,"\n","")
	reply_regex = r'<div class=\"content\">(.*?)href=\"\/(.*?)\"(.*?)data-user-id=\"(\d+)\"(.*?)avatar\"(.*?)src=\"(.*?)\"(.*?)href=\"(.*?)\/status\/(\d+)\"(.*?)data-time=\"(\d+)\"(.*?)tweet-text\">(.*?)<\/p>'
	reply_matches = re.findall(reply_regex,html)
	for match in reply_matches:
		reply = {}
		reply["user_id"] = int(match[3])
		reply["user_name"] = "@" + str(match[1]).lower()
		reply["avatar_url"] = str(match[6])		
		reply["tweet_id"] = int(match[9])
		reply["timestamp"] = int(match[11])
		reply["tweet_text"] = strip_tags(str(match[13]))
		replies.append(reply)

	return replies

def get_remote_tweet(user_name, tweet_id, system_path, tweet_data):
	file_name = system_path + "/" + str(user_name) + "_" + str(tweet_id) + ".json"
	try:
		f = open(file_name, 'r')
		print "Loading from file Cache"
		json_text = f.read()
	except:
		print "Fetching from Twitter"
		retweet_regex = re.compile("Retweets <strong>(.*?)</strong>")
		favorite_regex = re.compile("Favorites <strong>(\d+)<\/strong>")
		user_regex = r'data-user-id="(\d+)"(.*?)data-screen-name="(.*?)"(.*?)data-name="(.*?)"(.*?)profile-avatar(.*?)src="(.*?)"(.*?)strong(\d+)\/strong Followers'
		url = "https://twitter.com/" + str(user_name) + "/status/" + str(tweet_id)
		r = requests.get(url)
		output = r.text.encode("utf-8")

		retweet_matches = retweet_regex.search(output)
		if retweet_matches:
			num_retweets = int(string.replace(retweet_matches.group(1),",",""))
		else:
			num_retweets = 0

		favorite_matches = favorite_regex.search(output)
		if favorite_matches:
			num_favorites = int(string.replace(favorite_matches.group(1),",",""))
		else:
			num_favorites = 0

		retweeters = []
		if num_retweets > 0:
			retweets_list_url = "https://twitter.com/i/activity/retweeted_popup?id=" + str(tweet_id)
			r = requests.get(retweets_list_url)
			retweets_output = r.text.encode("utf-8")
			retweets_output = string.replace(retweets_output,"\u003C","")
			retweets_output = string.replace(retweets_output,"\u003E","")
			retweets_output = string.replace(retweets_output,"\\n","")
			retweets_output = string.replace(retweets_output,"\\","")
			user_matches = re.findall(user_regex,retweets_output)
			for matches in user_matches:
				user = {}
				user["user_id"] = int(matches[0])
				user["user_name"] = "@" + str(matches[2]).lower()
				user["display_name"] = str(matches[4])
				user["avatar_url"] = str(matches[7])
				user["num_followers"] = int(matches[9])
				retweeters.append(user)

		favoriters = []
		if num_favorites > 0:
			favorites_list_url = "https://twitter.com/i/activity/favorited_popup?id=" + str(tweet_id)
			r = requests.get(favorites_list_url)
			favorites_output = r.text.encode("utf-8")
			favorites_output = string.replace(favorites_output,"\u003C","")
			favorites_output = string.replace(favorites_output,"\u003E","")
			favorites_output = string.replace(favorites_output,"\\n","")
			favorites_output = string.replace(favorites_output,"\\","")
			user_matches = re.findall(user_regex,favorites_output)
			for matches in user_matches:
				user = {}
				user["user_id"] = int(matches[0])
				user["user_name"] = "@" + str(matches[2]).lower()
				user["display_name"] = str(matches[4])
				user["avatar_url"] = str(matches[7])
				user["num_followers"] = int(matches[9])
				favoriters.append(user)

		replies = get_replies(output)
		num_replies = len(replies)

		tweet_data["num_retweets"] = num_retweets
		tweet_data["retweeters"] = retweeters
		tweet_data["num_favorites"] = num_favorites
		tweet_data["favoriters"] = favoriters
		tweet_data["num_replies"] = num_replies
		tweet_data["replies"] = replies

		json_text = json.dumps(tweet_data)
		f = open(file_name, 'w')
		f.write(json_text)
		f.close()
		
	tweet_data = json.loads(json_text)
	return tweet_data


### BEGIN PROCEDURAL CODE ###

with open(path, mode='r') as infile:
	reader = csv.reader(infile)
	for row in reader:
		if rownum == 0:
			for i in range(len(row)):
				labels.append(row[i])
		else:
			tweet = {}
			for i in range(len(row)):
				#print i
				try:
					label = labels[i]
				except IndexError:
					label = "<UNKNOWN>"
				tweet[label] = row[i]
			tweets.append(tweet)
		rownum += 1


total_num_tweets = len(tweets)
i = 0

for single_tweet in reversed(tweets):
	i += 1
	print str(i) + " of " + str(total_num_tweets) + " - " + str(single_tweet["tweet_id"])	
	single_tweet = get_remote_tweet(twitter_username,single_tweet["tweet_id"],output_path,single_tweet)
	print single_tweet
	tweet_text = single_tweet["text"].lower()
	tweet_text_raw = tweet_text
	tweet_mentions = re.findall(mention_regex,tweet_text)
	for single_mention in tweet_mentions:
		tweet_text_raw = string.replace(tweet_text_raw,single_mention,"")
		if single_mention in mentions:
			mentions[single_mention] += 1
		else:
			mentions[single_mention] = 1

	tweet_hashtags = re.findall(hashtag_regex,tweet_text)
	for single_hashtag in tweet_hashtags:
		tweet_text_raw = string.replace(tweet_text_raw,single_hashtag,"")
		if single_hashtag in hashtags:
			hashtags[single_hashtag] += 1
		else:
			hashtags[single_hashtag] = 1
	try:
		tweet_words = nltk.word_tokenize(tweet_text_raw)
		for single_word in tweet_words:
			if single_word in words: #Optimiztion - no need to check regex or against stopwords if it's already in our words dict
				words[single_word] += 1
			else:
				if re.match(word_regex,single_word):
					try:
						if single_word not in stop_words:
							words[single_word] = 1
					except:
						pass
	except:
		pass 

sorted_mentions = sorted(mentions.items(), key=itemgetter(1), reverse=True)
sorted_mentions = sorted_mentions[0:20]
for idx, mention_user in enumerate(sorted_mentions):
	rank = str(idx + 1)
	print rank + ": " + mention_user[0] + " (" + str(mention_user[1]) + ")"

print "\n"

sorted_hashtags = sorted(hashtags.items(), key=itemgetter(1), reverse=True)
sorted_hashtags = sorted_hashtags[0:20]
for idx, mention_hashtag in enumerate(sorted_hashtags):
	rank = str(idx + 1)
	print rank + ": " + mention_hashtag[0] + " (" + str(mention_hashtag[1]) + ")"

print "\n"

sorted_words = sorted(words.items(), key=itemgetter(1), reverse=True)
sorted_words = sorted_words[0:10]
for idx, mention_word in enumerate(sorted_words):
	rank = str(idx + 1)
	print rank + ": " + str(mention_word[0]) + " (" + str(mention_word[1]) + ")"

print "\n"


