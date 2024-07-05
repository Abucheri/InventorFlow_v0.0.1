"""
Entry point into the system
"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'], strict_slashes=False)
def home():
	return render_template('index.html')

@app.route('/category', methods = ['GET', 'POST'], strict_slashes=False)
def categories():
	pass

@app.route('/suppliers', methods = ['GET', 'POST'], strict_slashes=False)
def suppliers():
	pass

@app.route('/transactions', methods = ['GET', 'POST'], strict_slashes=False)
def transactions():
	pass

@app.route('/summary', methods = ['GET'], strict_slashes=False)
def summary():
	pass


if __name__ == '__main__':
	app.run(debug=True)