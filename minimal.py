from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ridiculous')
def rid():
	return 'ridiculous!'

@app.route('/echo/<user>')
def echo(user):
	return 'Hello ' + user

@app.route('/ind')
def ind():
	return url_for('echo', user='bob')
