from config import config
from flask_oauth import OAuth

def get_twitter_oauth():
	oauth = OAuth()
	twitter = oauth.remote_app('twitter',
		base_url = '',
		request_token_url=config.get('TWITTER','REQUEST_TOKEN_URL'),
		access_token_url=config.get('TWITTER','ACCESS_TOKEN_URL'),
		authorize_url=config.get('TWITTER','AUTHORIZE_URL'),
		consumer_key=config.get('TWITTER','CONSUMER_KEY'),
		consumer_secret=config.get('TWITTER','CONSUMER_SECRET')
	)

	return twitter
