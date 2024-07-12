# InventorFlowv0.0.1

This is a stock management module for an inventory system.

## Installation

- Install python 3
```python
pip install -r requirements.txt
```
- You are all set.
- The file `helper_functions.py` has helper functions for formatting the dates from the db and the one from the UI. It also has a decorator for Authentication and Authentication session management.
- In `db.yaml`, configure your `database credentials` and `secret_key` to use in the app
- Use `secret_key_generator.py` to generate a secret key that you will copy to `db.yaml`. It has three options to choose from, choose according to you desire.
- use `data_manager.py` to interact and test db functionalities before implementing them in the app.

## Table Relations
- `products` is related to `categories`, `suppliers`, `units` and `categories` via `Foreign Keys`.
- `products` has a trigger to insert data into transactions whenever a product is made.
- You cannot delete from `categories`, `suppliers` and `units` without deleting there related children in products like:
```python
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
```