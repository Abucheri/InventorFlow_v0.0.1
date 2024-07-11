"""
Entry point into the system
"""

from flask import Flask, render_template

app = Flask(__name__)


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
