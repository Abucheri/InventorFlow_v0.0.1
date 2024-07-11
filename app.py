"""
Entry point into the system
"""

from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_mysqldb import MySQL
from helper_functions import updated_date, format_time_from_UI, login_required, Pagination
# from pytz import utc
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import yaml

app = Flask(__name__)
with open('db.yaml', 'r') as f:
    db = yaml.load(f, Loader=yaml.FullLoader)

# Set the secret key
app.config['SECRET_KEY'] = db['mysql_secret_key']

# MySQL Configuration
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

# Initialize MySQL
mysql = MySQL(app)


@app.route('/', methods=['GET'], strict_slashes=False)
@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    """
    Main products management page.
    """
    return render_template('home.html')


@app.route('/categories', methods=['GET', 'POST'], strict_slashes=False)
def categories():
    """
    Categories management page.
    """
    return render_template('category.html')


@app.route('/suppliers', methods=['GET', 'POST'], strict_slashes=False)
def suppliers():
    """
    Suppliers management page.
    """
    return render_template('suppliers.html')


@app.route('/products', methods=['GET'], strict_slashes=False)
def products():
    """
    Products management page
    """
    return render_template('index.html')


@app.route('/units', methods=['GET'], strict_slashes=False)
def units():
    """
    units management page.
    """
    return render_template('units.html')


@app.route('/transactions', methods=['GET', 'POST'], strict_slashes=False)
def transactions():
    """
    Transactions Management page.
    """
    return render_template('transactions.html')


@app.route('/summary', methods=['GET'], strict_slashes=False)
def summary():
    """
    Reports and Analysis page.
    """
    return render_template('summary.html')


if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)
