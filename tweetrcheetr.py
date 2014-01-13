import sys
from config import config
from flask import Flask
from flask import request
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def hello():
	print config.get('TWITTER','TWITTER_API_KEY')
	#return request.args.get('a');
	#return "Helloo"

hello()

#if __name__ == "__main__":
#	app.run(host='www.tweetrcheetr.com', port=8080)
