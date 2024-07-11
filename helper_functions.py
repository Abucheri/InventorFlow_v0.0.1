from datetime import datetime
from flask import flash, redirect, url_for, session
from functools import wraps

def updated_date():
    "update updated_at column for all tables after update"
    update_time = datetime.now()
    formattedd_time = format(update_time, "%Y-%m-%d %H:%M:%S")
    return_to_datetime_format = datetime.strptime(formattedd_time, "%Y-%m-%d %H:%M:%S")
    return return_to_datetime_format

def format_time_from_db(created_at):
    """Converts datetime format from DB to be displayed in HTML"""
    formated_time = format(created_at, "%Y-%m-%d")
    return formated_time

def format_time_from_UI(created_at):
    """Converts string datetime from UI to datetime to insert into DB"""
    new_format = created_at[0:10] + " " + created_at[11:]
    db_formatted_date = datetime.strptime(new_format, "%Y-%m-%d %H:%M")
    return db_formatted_date

def fromat_date_from_UI_using_replace(created_at):
    """format date string fro UI using replace to remove T between date and time"""
    new_date = created_at.replace('T', ' ')
    return new_date

# Function to protect routes
# def login_required(f):
#     """Login required decorator that ensures a user must be logged in in order to perform CRUD operations"""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             flash('You need to be logged in to access this page.', 'danger')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# def login_required(role='admin'):
#     """Protects routes based on user roles"""
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             print(f"Session Role: {session.get('role')}")
#             # if 'user_id' not in session or session['role'] != role:
#             if 'user_id' not in session or session.get('role') != role:
#                 flash('Unauthorized access. Please log in as admin.', 'danger')
#                 return redirect(url_for('login'))
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

def login_required(allowed_roles=['admin']):
    """Protects routes based on user roles"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Session Role: {session.get('role')}")
            if 'user_id' not in session or session.get('role') not in allowed_roles:
                flash('Unauthorized access. Please log in with appropriate permissions.', 'danger')
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator

class Pagination:
    def __init__(self, page, per_page, total, items):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        self.pages = (total + per_page - 1) // per_page
        self.has_next = page < self.pages
        self.has_prev = page > 1
        self.next_num = page + 1
        self.prev_num = page - 1