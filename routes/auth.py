from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from sqlalchemy import func
from extensions import db
from models import User
from services.finance_service import seed_default_categories

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated: return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip(); email = request.form.get("email", "").strip().lower(); password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter a name, valid email, and password of at least 8 characters.", "danger"); return render_template("register.html")
        if db.session.query(User).filter(func.lower(User.email) == email).first():
            flash("An account with that email already exists.", "warning"); return render_template("register.html")
        user = User(name=name, email=email); user.set_password(password); db.session.add(user); db.session.commit(); seed_default_categories(user.id, db); login_user(user)
        return redirect(url_for("main.dashboard"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower(); password = request.form.get("password", "")
        user = db.session.query(User).filter(func.lower(User.email) == email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger"); return render_template("login.html")
        login_user(user); return redirect(request.args.get("next") or url_for("main.dashboard"))
    return render_template("login.html")

@auth_bp.post("/logout")
def logout():
    logout_user(); return redirect(url_for("auth.login"))
