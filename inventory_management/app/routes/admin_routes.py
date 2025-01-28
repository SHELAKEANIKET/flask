from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.admin import Admin
from flask_bcrypt import Bcrypt

admin_bp = Blueprint('admin', __name__)

bcrypt = Bcrypt()

# Admin login route
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        admin = Admin.login_admin(email)

        if admin and bcrypt.check_password_hash(admin[2], password):  # Password hash comparison
            session["username"] = admin[0]
            
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for("admin.login"))
        
    return render_template("login.html")

# Admin logout route
@admin_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("admin.login"))
