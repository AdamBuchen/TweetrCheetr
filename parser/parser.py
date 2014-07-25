import csv, re, nltk, string
from operator import itemgetter
from nltk.corpus import stopwords

path = "tweets.csv"
stop_words = stopwords.words('english')
stop_words.append('http')

labels = []
tweets = []
rownum = 0;
mentions = {}
hashtags = {}
words = {}

print "\n"

##regexes
mention_regex = "\@[A-Za-z0-9_]+"
hashtag_regex = "\#[A-Za-z0-9_]+"
word_regex = "[A-Za-z][A-Za-z0-9_-]+"

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


for single_tweet in reversed(tweets):
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
