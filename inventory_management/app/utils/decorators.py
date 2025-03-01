from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("You need to log in first.", "warning")
            return redirect(url_for("admin.login"))  # Ensure this points to your login route
        return f(*args, **kwargs)
    return decorated_function
