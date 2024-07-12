"""
Entry point into the system
"""

from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_mysqldb import MySQL
from helper_functions import updated_date, format_time_from_UI, login_required, Pagination
from pytz import utc
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

# Session timeout configuration (30 minutes)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Initialize MySQL
mysql = MySQL(app)

# Middleware to handle session timeout
@app.before_request
def before_request():
    if 'user_id' in session:
        last_activity = session.get('last_activity')

        # Ensure last_activity is timezone-aware (assuming UTC for example)
        if isinstance(last_activity, datetime):
            last_activity = last_activity.replace(tzinfo=utc)

        # Check if session expired due to inactivity
        if last_activity is not None and datetime.now(utc) > last_activity + app.permanent_session_lifetime:
            session.clear()
            flash('Your session has expired due to inactivity. Please log in again.', 'info')
            return redirect(url_for('login'))

        # Update last activity time for the session
        session['last_activity'] = datetime.now(utc)

@app.route('/', methods=['GET'], strict_slashes=False)
@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    """
    Main homepage/landing page.
    """
    if 'user_name' in session:
        return render_template('home.html', user_name=session['user_name'])
    else:
        return render_template('home.html')

# =======AUTH operations=======
@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():  # put application's code here
    """Login functionality route"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['role'] = user[4]  # role is stored in the 5th column (index 4)
            session['last_activity'] = datetime.now(utc)  # Set initial last activity
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))  # Redirect to login again on failure

    # Handle GET request (show login form)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():  # put application's code here
    """Register new users to db with name, email and passwword"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        confirm_password = request.form['c_pass']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        # insert query
        cursor = mysql.connection.cursor()
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)",
                       (str(uuid4()), name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout', methods=['GET'], strict_slashes=False)
def logout():  # put application's code here
    """Logout users from platform"""
    # Clear session data
    # session.pop('user_id', None)
    # session.pop('user_name', None)
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# CRUD operations
# =======categories=======
@app.route('/categories', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def categories():
    """
    Categories management page.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search_query = request.args.get('search', '')

    cursor = mysql.connection.cursor()

    if search_query:
        search_sql = "SELECT * FROM categories WHERE name LIKE %s ORDER BY name ASC"
        cursor.execute(search_sql, ('%' + search_query + '%',))
    else:
        search_sql = "SELECT * FROM categories ORDER BY name ASC"
        cursor.execute(search_sql)

    categories = cursor.fetchall()
    cursor.close()

    # Paginate the results manually
    total = len(categories)
    categories = categories[(page - 1) * per_page:page * per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, items=categories)

    return render_template('category.html', categories=pagination)

@app.route('/add_categories', methods=['POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def add_category():
    """Add categories to database"""
    if request.method == 'POST':
        name = request.form['category_name']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO categories (id, name) VALUES (%s, %s)", (str(uuid4()), name))
        mysql.connection.commit()
        cursor.close()
        flash(f'Category "{name}" added successfully!', 'success')
        return redirect(url_for('categories'))


@app.route('/edit_category/<id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def edit_category(id):
    """Update categories by ID"""
    if request.method == 'POST':
        name = request.form['category_name']
        update_time = updated_date()

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE categories SET name = %s, updated_at = %s WHERE id = %s", (name, update_time, id))
        mysql.connection.commit()
        cursor.close()

        flash(f'Category "{name}" updated successfully!', 'success')
        return redirect(url_for('categories'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = %s", (id,))
        category = cursor.fetchone()
        cursor.close()
        return render_template('edit_category.html', category=category)

@app.route('/delete_category/<id>', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def delete_category(id):
    """Delete categories by ID"""
    cursor = mysql.connection.cursor()

    # First, check if there are any products using this category
    cursor.execute("SELECT * FROM products WHERE product_category_id = %s", (id,))
    products_using_category = cursor.fetchall()

    if products_using_category:
        # If there are products, you might choose to delete or update them
        # For example, delete all products using this category
        cursor.execute("DELETE FROM products WHERE product_category_id = %s", (id,))
        mysql.connection.commit()
    cursor.execute("SELECT name FROM categories WHERE id = %s", (id,))
    category_name = cursor.fetchone()[0]
    cursor.execute("DELETE FROM categories WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash(f'Category "{category_name}" deleted successfully!', 'success')
    return redirect(url_for('categories'))

# =======units=======
@app.route('/units', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def units():
    """Retrieve Units of measurement"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search_query = request.args.get('search', '')

    cursor = mysql.connection.cursor()

    if search_query:
        search_sql = "SELECT * FROM units WHERE unit LIKE %s ORDER BY unit ASC"
        cursor.execute(search_sql, ('%' + search_query + '%',))
    else:
        search_sql = "SELECT * FROM units ORDER BY unit ASC"
        cursor.execute(search_sql)

    units = cursor.fetchall()
    cursor.close()

    # Paginate the results manually
    total = len(units)
    units = units[(page - 1) * per_page:page * per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, items=units)

    return render_template('units.html', units=pagination)

@app.route('/add_units', methods=['POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def add_unit():
    """Add units to database"""
    if request.method == 'POST':
        unit_name = request.form['unit_name']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO units (id, unit) VALUES (%s, %s)", (str(uuid4()), unit_name))
        mysql.connection.commit()
        cursor.close()
        flash(f'Unit "{unit_name}" added successfully!', 'success')
        return redirect(url_for('units'))

@app.route('/edit_unit/<id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def edit_unit(id):
    """Update units by ID"""
    if request.method == 'POST':
        unit_name = request.form['unit_name']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE units SET unit = %s, updated_at = %s WHERE id = %s", (unit_name, updated_date(), id))
        mysql.connection.commit()
        cursor.close()
        flash(f'Unit "{unit_name}" updated successfully!', 'success')
        return redirect(url_for('units'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM units WHERE id = %s", (id,))
        unit = cursor.fetchone()
        cursor.close()
        return render_template('edit_unit.html', unit=unit)

@app.route('/delete_unit/<id>', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def delete_unit(id):
    """Delete units by ID"""
    cursor = mysql.connection.cursor()

    # First, check if there are any products using this Unit
    cursor.execute("SELECT * FROM products WHERE product_unit_id = %s", (id,))
    products_using_unit = cursor.fetchall()

    if products_using_unit:
        # If there are products, you might choose to delete or update them
        # For example, delete all products using this category
        cursor.execute("DELETE FROM products WHERE product_unit_id = %s", (id,))
        mysql.connection.commit()
    cursor.execute("SELECT unit FROM units WHERE id = %s", (id,))
    unit_name = cursor.fetchone()[0]
    cursor.execute("DELETE FROM units WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash(f'Unit "{unit_name}" deleted successfully!', 'success')
    return redirect(url_for('units'))

# =======Suppliers=======
@app.route('/suppliers', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def suppliers():
    """Displays Suppliers details"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search_query = request.args.get('search', '')

    cursor = mysql.connection.cursor()

    if search_query:
        search_sql = "SELECT * FROM suppliers WHERE supplier_name LIKE %s ORDER BY supplier_name ASC"
        cursor.execute(search_sql, ('%' + search_query + '%',))
    else:
        search_sql = "SELECT * FROM suppliers ORDER BY supplier_name ASC"
        cursor.execute(search_sql)

    suppliers = cursor.fetchall()
    cursor.close()

    # Paginate the results manually
    total = len(suppliers)
    suppliers = suppliers[(page - 1) * per_page:page * per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, items=suppliers)

    return render_template('suppliers.html', suppliers=pagination)

@app.route('/add_suppliers', methods=['POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def add_supplier():
    """Adds a new supplier to DB"""
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        supplier_contact = request.form['supplier_contact']
        supplier_agreement = request.form['supplier_agreement']
        supplier_date = format_time_from_UI(request.form['supplier_date'])
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO suppliers (id, supplier_name, supplier_contact, supplier_agreement, created_at) VALUES (%s, %s, %s, %s, %s)", (str(uuid4()), supplier_name, supplier_contact, supplier_agreement, supplier_date))
        mysql.connection.commit()
        cursor.close()
        flash(f'Supplier "{supplier_name}" added successfully!', 'success')
        return redirect(url_for('suppliers'))


@app.route('/edit_suppliers/<id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def edit_suppliers(id):
    """Updates Supplier details"""
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        supplier_contact = request.form['supplier_contact']
        supplier_agreement = request.form['supplier_agreement']
        updated = updated_date()
        sql = "UPDATE suppliers SET "
        params = []

        if supplier_name:
            sql += "supplier_name = %s, updated_at = %s, "
            params.append(supplier_name)
            params.append(updated)
        if supplier_contact:
            sql += "supplier_contact = %s, updated_at = %s, "
            params.append(supplier_contact)
            params.append(updated)
        if supplier_agreement:
            sql += "supplier_agreement = %s, updated_at = %s, "
            params.append(supplier_agreement)
            params.append(updated)

        # Remove the trailing comma and space
        sql = sql.rstrip(', ')
        sql += " WHERE id = %s"
        params.append(id)

        cursor = mysql.connection.cursor()
        cursor.execute(sql, tuple(params))
        mysql.connection.commit()
        cursor.close()
        flash(f'Supplier "{supplier_name}" updated successfully!', 'success')
        return redirect(url_for('suppliers'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM suppliers WHERE id = %s", (id,))
        supplier = cursor.fetchone()
        cursor.close()
        return render_template('edit_supplier.html', supplier=supplier)

@app.route('/delete_suppliers/<id>', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def delete_suppliers(id):
    """Deletes supplier from DB by ID"""
    cursor = mysql.connection.cursor()

    # First, check if there are any products using this Supplier
    cursor.execute("SELECT * FROM products WHERE product_supplier_id = %s", (id,))
    products_using_unit = cursor.fetchall()

    if products_using_unit:
        # If there are products, you might choose to delete or update them
        # For example, delete all products using this category
        cursor.execute("DELETE FROM products WHERE product_supplier_id = %s", (id,))
        mysql.connection.commit()
    cursor.execute("SELECT supplier_name FROM suppliers WHERE id = %s", (id,))
    supplier_name = cursor.fetchone()[0]
    cursor.execute("DELETE FROM suppliers WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash(f'Supplier "{supplier_name}" deleted successfully!', 'success')
    return redirect(url_for('suppliers'))

# =======products=======
@app.route('/products', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def products():
    """Displays all products with their relevant details or search results with pagination"""
    cursor = mysql.connection.cursor()

    # Get the search query and page number from the request arguments
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Fetch categories, units, and suppliers for the dropdowns
    cursor.execute("SELECT id, name FROM categories ORDER BY name ASC")
    categories = cursor.fetchall()

    cursor.execute("SELECT id, unit FROM units ORDER BY unit ASC")
    units = cursor.fetchall()

    cursor.execute("SELECT id, supplier_name FROM suppliers ORDER BY supplier_name ASC")
    suppliers = cursor.fetchall()

    # Base SQL query
    base_sql = """
    SELECT p.id, p.product_name AS name, c.name AS category, u.unit AS unit, p.description AS description, p.price AS price, p.quantity AS quantity, 
        s.supplier_name AS supplier, p.created_at AS create_date
    FROM products AS p
    LEFT JOIN categories AS c
        ON p.product_category_id = c.id
    LEFT JOIN units AS u
        ON p.product_unit_id = u.id
    LEFT JOIN suppliers AS s
        ON p.product_supplier_id = s.id
    """

    # Modify the query if there is a search query
    if search_query:
        search_sql = base_sql + " WHERE p.product_name LIKE %s OR c.name LIKE %s OR u.unit LIKE %s OR s.supplier_name LIKE %s ORDER BY p.created_at DESC LIMIT %s OFFSET %s"
        search_param = f"%{search_query}%"
        cursor.execute(search_sql, (search_param, search_param, search_param, search_param, per_page, offset))
    else:
        pagination_sql = base_sql + " ORDER BY p.created_at DESC LIMIT %s OFFSET %s"
        cursor.execute(pagination_sql, (per_page, offset))

    products = cursor.fetchall()

    # Get the total number of products for pagination
    if search_query:
        count_sql = "SELECT COUNT(*) FROM products AS p LEFT JOIN categories AS c ON p.product_category_id = c.id LEFT JOIN units AS u ON p.product_unit_id = u.id LEFT JOIN suppliers AS s ON p.product_supplier_id = s.id WHERE p.product_name LIKE %s OR c.name LIKE %s OR u.unit LIKE %s OR s.supplier_name LIKE %s"
        cursor.execute(count_sql, (search_param, search_param, search_param, search_param))
    else:
        count_sql = "SELECT COUNT(*) FROM products"
        cursor.execute(count_sql)

    total_products = cursor.fetchone()[0]
    total_pages = (total_products + per_page - 1) // per_page

    cursor.close()

    return render_template('index.html', categories=categories, units=units, suppliers=suppliers, products=products, search_query=search_query, page=page, total_pages=total_pages)

@app.route('/add_products', methods=['POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def add_products():
    """Adds new product into the DB"""
    if request.method == 'POST':
        p_name = request.form['p_name']
        p_category = request.form['p_category']
        p_unit = request.form['p_unit']
        p_desc = request.form['p_desc']
        p_price = float(request.form['p_price'])
        p_quantity = request.form['p_quantity']
        p_supplier = request.form['p_supplier']
        p_date = format_time_from_UI(request.form['p_date'])
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO products (id, product_name, product_category_id, product_unit_id, description, price, quantity, product_supplier_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (str(uuid4()), p_name, p_category, p_unit, p_desc, p_price, p_quantity, p_supplier, p_date))
        mysql.connection.commit()
        cursor.close()
        flash(f'Product "{p_name}" added successfully!', 'success')
        return redirect(url_for('products'))


@app.route('/edit_products/<id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required(['admin', 'user'])
def edit_products(id):
    """Updates products by ID"""
    if request.method == 'POST':
        p_name = request.form['p_name']
        p_category = request.form['p_category']
        p_unit = request.form['p_unit']
        p_desc = request.form['p_desc']
        p_price = float(request.form['p_price'])
        p_quantity = request.form['p_quantity']
        p_supplier = request.form['p_supplier']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE products SET product_name = %s, product_category_id = %s, product_unit_id = %s, description = %s, price = %s, quantity = %s, product_supplier_id = %s, updated_at = %s WHERE id = %s
        """, (p_name, p_category, p_unit, p_desc, p_price, p_quantity, p_supplier, updated_date(), id))

        mysql.connection.commit()
        cursor.close()
        flash(f'Product "{p_name}" updated successfully!', 'success')
        return redirect(url_for('products'))
    else:
        cursor = mysql.connection.cursor()

        # Fetch the product details
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()

        # Fetch categories, units, and suppliers for dropdowns
        cursor.execute("SELECT id, name FROM categories ORDER BY name ASC")
        categories = cursor.fetchall()

        cursor.execute("SELECT id, unit FROM units ORDER BY unit ASC")
        units = cursor.fetchall()

        cursor.execute("SELECT id, supplier_name FROM suppliers ORDER BY supplier_name ASC")
        suppliers = cursor.fetchall()

        cursor.close()
        return render_template('edit_products.html', product=product, categories=categories, units=units,
                               suppliers=suppliers)

@app.route('/delete_product/<id>', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def delete_product(id):
    """Delete product by ID"""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT product_name FROM products WHERE id = %s", (id,))
    product_name = cursor.fetchone()[0]
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash(f'Product "{product_name}" deleted successfully!', 'success')
    return redirect(url_for('products'))

# =======transactions page=======
# Add this route to display the transactions page
@app.route('/transactions', methods=['GET'], strict_slashes=False)
@login_required(['admin', 'user'])
def transactions():
    """Displays all transactions with their relevant details or search results with pagination"""
    cursor = mysql.connection.cursor()

    # Get the search query and page number from the request arguments
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Base SQL query
    base_sql = """
    SELECT t.id, t.product_name, t.price, t.quantity, s.supplier_name, t.created_at 
    FROM transactions AS t
    LEFT JOIN suppliers AS s ON t.supplier_name_id = s.id
    """

    # Modify the query if there is a search query
    if search_query:
        search_sql = base_sql + " WHERE t.product_name LIKE %s OR s.supplier_name LIKE %s ORDER BY t.created_at DESC LIMIT %s OFFSET %s"
        search_param = f"%{search_query}%"
        cursor.execute(search_sql, (search_param, search_param, per_page, offset))
    else:
        pagination_sql = base_sql + " ORDER BY t.created_at DESC LIMIT %s OFFSET %s"
        cursor.execute(pagination_sql, (per_page, offset))

    transactions = cursor.fetchall()

    # Get the total number of transactions for pagination
    if search_query:
        count_sql = "SELECT COUNT(*) FROM transactions AS t LEFT JOIN suppliers AS s ON t.supplier_name_id = s.id WHERE t.product_name LIKE %s OR s.supplier_name LIKE %s"
        cursor.execute(count_sql, (search_param, search_param))
    else:
        count_sql = "SELECT COUNT(*) FROM transactions"
        cursor.execute(count_sql)

    total_transactions = cursor.fetchone()[0]
    total_pages = (total_transactions + per_page - 1) // per_page

    cursor.close()

    return render_template('transactions.html', transactions=transactions, search_query=search_query, page=page, total_pages=total_pages)

if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)
