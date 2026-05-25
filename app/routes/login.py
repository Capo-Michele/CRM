from flask import Flask, render_template, Blueprint, request, redirect, flash, url_for
from app.extensions import db
from app.models import User
from math import ceil
from flask_login import current_user
from flask_login import login_user, logout_user

bp = Blueprint('login', __name__)


@bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('client_page.client'))
    
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            flash("Username or email already registered")
            return redirect (url_for('login.login'))
        else:
            new_user = User(username=username, email=email, )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login.login'))

    return render_template ('register.html')

@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('You have successfully logged in')
            return redirect(url_for('client_page.client'))
        else:
            flash('Invalid password')
            return redirect(url_for('login.login'))
    return render_template ('login.html')


@bp.route('/logout')
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('main.index'))


