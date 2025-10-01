from flask import Blueprint, render_template, redirect, session, request, url_for, flash, send_file, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import base64
from io import BytesIO
import os

from user.models import User, Blocked
from admin.models import Celebrity
from application import db

user_app = Blueprint('user_app', __name__)


@user_app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')


@user_app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).one()
        if user:
            session['username'] = username
            session['email'] = user.email
            block_check = Blocked.query.filter_by(user_id=user.user_id).first()
            if block_check:
                flash('You are blocked by the admin..., please try later or contact him')
                return redirect(url_for('user_app.user_login'))
            return redirect(url_for('user_app.user_dashboard'))
        else:
            flash('Invalid user please enter valid credentials or register')
    return render_template('user_login.html')


@user_app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        c_password = request.form.get('confirm_password')
        if password == c_password:
            user = User(
                username=username,
                password=password,
                email=email
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user_app.user_login'))
        else:
            flash('Password and confirm password are different please try again...')

    return render_template('user_register.html')


@user_app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    search_query = None

    # If user submits search form
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        if search_query:
            # Filter celebrities by name or category (case-insensitive)
            all_celebrities = Celebrity.query.filter(
                (Celebrity.celebrity_name.ilike(f"%{search_query}%")) |
                (Celebrity.category.ilike(f"%{search_query}%"))
            ).all()
        else:
            all_celebrities = Celebrity.query.all()
    else:
        # Default: load all celebrities
        all_celebrities = Celebrity.query.all()

    celebrities_with_images = []
    for celebrity in all_celebrities:
        profile_base64 = None
        if celebrity.profile:
            profile_base64 = base64.b64encode(celebrity.profile).decode('utf-8')

        celebrities_with_images.append({
            'celebrity_name': celebrity.celebrity_name,
            'category': celebrity.category,
            'Insta': celebrity.Insta,
            'yt': celebrity.yt,
            'twitter': celebrity.twitter,
            'profile_base64': profile_base64
        })

    return render_template(
        'user_dashboard.html',
        celebrities=celebrities_with_images,
        search_query=search_query
    )

