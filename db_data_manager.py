import mysql.connector
from uuid import uuid4
from datetime import datetime
import yaml


# Load the YAML configuration using yaml.FullLoader
# db = yaml.load(open('db.yaml'))
# Security Consideration: Always use yaml.FullLoader or yaml.
# SafeLoader to avoid potential security vulnerabilities associated with loading YAML in Python.
# File Handling: It's good practice to use with open(...) as f for file handling in Python,
# as it ensures the file is properly closed after use.
# try to use yaml.safe_load(yamlfile) instead of yaml.load(). And If you need FullLoader, you can use yaml.full_load(yamlfile).
with open('db.yaml', 'r') as f:
    db = yaml.load(f, Loader=yaml.FullLoader)


def updated_date():
    "update updated_at column for all tables after update"
    update_time = datetime.now()
    formattedd_time = format(update_time, "%Y-%m-%d %H:%M:%S")
    return_to_datetime_format = datetime.strptime(formattedd_time, "%Y-%m-%d %H:%M:%S")
    return return_to_datetime_format



class DBConnection:
    """DB connection class"""
    def __init__(self):
        self.conn = mysql.connector.Connect(
            host=db['mysql_host'],
            user=db['mysql_user'],
            password=db['mysql_password'],
            database=db['mysql_db']
        )
    
        self.cursor = self.conn.cursor()
    
    def user_insert(self, name, email, password):
        """Insert Users to DB"""
        sql = """INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)"""
        id = uuid4()
        id = str(id)
        vals = (id, name, email, password)
        
        try:
            self.cursor.execute(sql, vals)
            self.conn.commit()
            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def category_insert(self, name):
        """Insert a new category into the database."""
        sql = """INSERT INTO categories (id, name) VALUES (%s, %s)"""
        id = str(uuid4())  # Generate a new UUID and convert to string
        vals = (id, name)
        
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql, vals)
            self.conn.commit()
            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as e:
            print("Error inserting category:", e)
            self.conn.rollback()
        finally:
            # Close cursor in the finally block to ensure it's always executed
            if self.cursor:
                self.cursor.close()
                # self.conn.close()
    
    def category_select(self):
        """Retrieve category overview"""
        sql = """SELECT * FROM categories"""
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
            return []
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def category_update(self, name, id):
        """Categories update"""
        sql = """UPDATE categories SET name = %s WHERE id = %s"""
        id = id
        name = name
        
        try:
            self.cursor.execute(sql, (name, id))
            self.conn.commit()
            print(self.cursor.rowcount, "record updated.\n")
            print("entry updated in categories...")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def category_delete(self, id):
        """Categories delete"""
        sql = """DELETE FROM categories WHERE id  = %s"""
        id = id
        
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            print(self.cursor.rowcount, "record deleted.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def supplier_insert(self, name, contact, agreement):
        """Suppliers insert"""
        sql = """INSERT INTO suppliers (id, supplier_name, supplier_contact, supplier_agreement) VALUES (%s, %s, %s, %s)"""
        id = uuid4()
        id = str(id)
        vals = (id, name, contact, agreement)
        
        try:
            self.cursor.execute(sql, vals)
            self.conn.commit()
            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def supplier_update(self, id, name=None, contact=None, agreement=None):
        """Suppliers update"""
        if name:
            sql = """Update suppliers SET supplier_name = %s WHERE id = %s"""
        elif contact:
            sql = """Update suppliers SET supplier_contact = %s WHERE id = %s"""
        elif agreement:
            sql = """Update suppliers SET supplier_agreement = %s WHERE id = %s"""
        else:
            sql = """UPDATE suppliers SET supplier_name = %s, supplier_contact = %s, supplier_agreement = %s WHERE id = %s"""
        
        id = id
        name = name
        contact = contact
        agreement = agreement
        
        try:
            if name:
                self.cursor.execute(sql, (name, id))
            elif contact:
                self.cursor.execute(sql, (contact, id))
            elif agreement:
                self.cursor.execute(sql, (agreement, id))
            else:
                self.cursor.execute(sql, (name, contact, agreement, id))
            self.conn.commit()
            print(self.cursor.rowcount, "record(s) updated.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def supplier_delete(self, id):
        """Supplier delete"""
        sql = """DELETE FROM suppliers WHERE id  = %s"""
        id = id
        
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            print(self.cursor.rowcount, "record deleted.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
            
    def transaction_update(self, returned, id):
        """transaction returns update"""
        sql = """UPDATE transactions SET returned = %s WHERE id = %d"""
        id = id
        returned = returned
        
        try:
            self.cursor.execute(sql, (returned, id))
            self.conn.commit()
            print(self.cursor.rowcount, "record updated.\n")
            print("entry updated in categories...")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def products_select(self):
        """Retrieve products data from DB"""
        sql = """
        SELECT p.product_name AS name, c.name AS category, u.unit AS unit, p.description AS description, p.price AS price, p.quantity AS quantity, 
        s.supplier_name AS supplier, p.created_at AS create_date
        FROM products AS p
        LEFT JOIN categories AS c
        ON p.product_category_id = c.id
        LEFT JOIN units AS u
        ON p.product_unit_id = u.id
        LEFT JOIN suppliers AS s
        ON p.product_supplier_id = s.id
        ORDER BY p.created_at DESC
        """
        try:
            self.cursor.execute(sql)
            products = self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
            return []
        finally:
            self.cursor.close()
            return products
            
    def products_insert(self, name, category, description, price, quantity, unit, supplier):
        """Insert new product"""
        sql = """INSERT INTO products (id, product_name, product_category, description, price, quantity, unit, supplier_name)
              VALUES (%s, %s, %s, %s, %.2f, %d, %s, %s)"""
        id = uuid4()
        id = str(id)
        vals = (id, name, category, description, price, quantity, unit, supplier)
        
        try:
            self.cursor.execute(sql, vals)
            self.conn.commit()
            print(self.cursor.rowcount, "record updated.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def products_update(self, id, name=None, category=None , description=None, price=None, quantity=None, unit=None, supplier=None):
        """Update product"""
        if name:
            sql = """UPDATE products SET product_name = %s WHERE id = %s"""
        elif category:
            sql = """UPDATE products SET product_category = %s WHERE id = %s"""
        elif description:
            sql = """UPDATE products SET description = %s WHERE id = %s"""
        elif price:
            sql = """UPDATE products SET price = %.2f WHERE id = %s"""
        elif quantity:
            sql = """UPDATE products SET quantity = %d WHERE id = %s"""
        elif unit:
            sql = """UPDATE products SET unit = %s WHERE id = %s"""
        elif supplier:
            sql = """UPDATE products SET supplier_name = %s WHERE id = %s"""
        else:
            sql = """UPDATE products SET product_name = %s, product_category = %s, description = %s, price = %.2f, quantity = %d, unit = %s, supplier_name = %s
                  WHERE id = %s"""
        id = id
        name = name
        category = category
        description = description
        price = price
        quantity = quantity
        unit = unit
        supplier = supplier
        
        try:
            if name:
                self.cursor.execute(sql, (name, id))
            elif category:
                self.cursor.execute(sql, (category, id))
            elif description:
                self.cursor.execute(sql, (description, id))
            elif price:
                self.cursor.execute(sql, (price, id))
            elif quantity:
                self.cursor.execute(sql, (quantity, id))
            elif unit:
                self.cursor.execute(sql, (unit, id))
            elif supplier:
                self.cursor.execute(sql, (supplier, id))
            else:
                self.cursor.execute(sql, (name, category, description, price, quantity, unit, supplier, id))
            self.conn.commit()
            print(self.cursor.rowcount, "record(s) updated.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def products_delete(self, id):
        """Products delete"""
        sql = """DELETE FROM products WHERE id  = %s"""
        id = id
        
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            print(self.cursor.rowcount, "record(s) deleted.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def unit_insert(self, unit):
        """Unit insert"""
        sql = """INSERT INTO units (id, unit) VALUES (%s, %s)"""
        id = uuid4()
        id = str(id)
        vals = (id, unit)
        
        try:
            self.cursor.execute(sql, vals)
            self.conn.commit()
            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def unit_update(self, id, unit):
        """Unit update"""
        sql = """UPDATE units SET unit = %s WHERE id = %s"""
        unit = unit
        
        try:
            self.cursor.execute(sql, (unit, id))
            self.conn.commit()
            print(self.cursor.rowcount, "record updated.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    def unit_delete(self, id):
        """Unit update"""
        sql = """DELETE FROM units WHERE id = %s"""
        
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            print(self.cursor.rowcount, "record deleted.")
        except mysql.connector.Error as e:
            print(e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            # self.conn.close()
    
    # select statements
        
# insert_cat = DBConnection()
# insert_cat.category_insert("MY NEW CAT")

fetch_products = DBConnection()
products = fetch_products.products_select()
for product in products:
    print(product)

