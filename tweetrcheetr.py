from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "Helloo"

if __name__ == "__main__":
	app.run(host='www.tweetrcheetr.com', port=8080)
