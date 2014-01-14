import sys
from twitter import twitter
from pprint import pprint
from config import config
from flask import Flask, request, render_template, make_response, Response, url_for, redirect, session, flash
from flask_oauth import OAuth

app = Flask(__name__)
app.secret_key = config.get('GENERAL','APP_SECRET_KEY')

@app.route("/")
def index():
	username = None
	if 'twitter_user' in session:
		username = session['twitter_user']
		
	return render_template('index.tpl',username=username)

@app.route("/login")
def login():
	return twitter.authorize(callback=url_for('callback',
		next=request.args.get('next') or request.referrer or None))

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route("/callback")
@twitter.authorized_handler
def callback(resp):
	next_url = request.args.get('next') or url_for('index')
	if resp is None:
		flash('You denied the request to sign in.')
		return redirect(next_url)

	session['twitter_token'] = (
		resp['oauth_token'],
		resp['oauth_token_secret']
	)

	session['twitter_user'] = resp['screen_name']

	flash('You were signed in as %s' % resp['screen_name'])
	return redirect(next_url)

@twitter.tokengetter
def get_twitter_token(token=None):
	return session.get('twitter_token')


if __name__ == "__main__":
	app.run(debug=True, host='www.tweetrcheetr.com', port=8080)
