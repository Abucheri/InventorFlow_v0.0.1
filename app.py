"""
Entry point into the system
"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """
    Main products management page.
    """
    return render_template('index.html')


@app.route('/category', methods=['GET', 'POST'], strict_slashes=False)
def categories():
    """
    Categories management page.
    """
    pass


@app.route('/suppliers', methods=['GET', 'POST'], strict_slashes=False)
def suppliers():
    """
    Suppliers management page.
    """
    pass


@app.route('/transactions', methods=['GET', 'POST'], strict_slashes=False)
def transactions():
    """
    Transactions Management page.
    """
    pass


@app.route('/summary', methods=['GET'], strict_slashes=False)
def summary():
    """
    Reports and Analysis page.
    """
    pass


if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)