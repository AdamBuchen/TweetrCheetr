import sys
import twitter
from pprint import pprint
from config import config
from flask import Flask, request, render_template, make_response, Response, url_for
from flask_oauth import OAuth

app = Flask(__name__)
app.secret_key = "THISISMYCUSTOMSECRETKEYANDILOVEIT"

@app.route("/")
def index():
	return render_template('index.tpl')
	#print config.get('TWITTER','TWITTER_API_KEY')
	#return request.args.get('a');
	#return "Helloo"

@app.route("/login")
def login():
	twitter_oauth = twitter.get_twitter_oauth()
	return twitter_oauth.authorize(callback=url_for('oauth_authorized',
		next=request.args.get('next') or request.referrer or None))

@app.route("/callback")
def callback():
	print "here"

@app.route('/oauth_authorized')
def oauth_authorized():
	print "here2"

if __name__ == "__main__":
	app.run(debug=True, host='www.tweetrcheetr.com', port=8080)
