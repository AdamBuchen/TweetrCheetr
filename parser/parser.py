import csv, re
from operator import itemgetter

path = "tweets.csv"
labels = []
tweets = []
rownum = 0;
mentions = {}

print "\n"

##regexes
mention_regex = "\@[A-Za-z0-9_]+"

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
	tweet_mentions = re.findall(mention_regex,tweet_text)
	for single_mention in tweet_mentions:
		if single_mention in mentions:
			mentions[single_mention] += 1
		else:
			mentions[single_mention] = 1

sorted_mentions = sorted(mentions.items(), key=itemgetter(1), reverse=True)
sorted_mentions = sorted_mentions[0:10]
for mention_user in sorted_mentions:
	print mention_user

print "\n"
