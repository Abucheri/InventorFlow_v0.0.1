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

# Initialize MySQL
mysql = MySQL(app)


@app.route('/', methods=['GET'], strict_slashes=False)
@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    """
    Main homepage/landing page.
    """
    return render_template('home.html')

# CRUD operations
# =======categories=======
@app.route('/categories', methods=['GET'], strict_slashes=False)
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


if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)
