from flask import Blueprint, render_template, redirect, session, request, url_for, flash, send_file, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import base64
from io import BytesIO
import os
from admin.models import Celebrity
from user.models import User, Blocked

#from self.models import Projects, Certifications, Work, Skills, Resume, Education
from application import db

admin_app = Blueprint('admin_app', __name__)


@admin_app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@admin_app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    return render_template('admin_dashboard.html')


@admin_app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == 'GS KI LEDH':
            flash('Welcome BOSS')
            return redirect(url_for('admin_app.admin_dashboard'))
        else:
            flash("'GS KI LEDH RA' JAFDA")
            return redirect(url_for('admin_app.admin_login'))
    return render_template('admin_login.html')


@admin_app.route('/add_celebrity', methods=['GET', 'POST'])
def add_celebrity():
    if request.method == 'POST':
        name = request.form.get('celebrity_name')
        category = request.form.get('category')
        insta = request.form.get('insta_link')
        yt = request.form.get('yt_link')
        twitter = request.form.get('twitter_link')
        image = None
        profile = request.files.get('profile_photo')
        if profile and profile.filename != '':
            image = profile.read()
            profile.seek(0)
        celebrity = Celebrity(
            celebrity_name=name,
            category=category,
            Insta=insta,
            yt=yt,
            twitter=twitter,
            profile=image
        )
        db.session.add(celebrity)
        db.session.commit()
        flash('Celebrity added successfully')
        return redirect(url_for('admin_app.admin_dashboard'))
    return render_template('add_celebrity.html')


@admin_app.route('/edit_celebrity', methods=['GET', 'POST'])
def edit_celebrity():
    celebrities = Celebrity.query.all()  # Fetch all celebrities

    if request.method == 'POST':
        celeb_id = request.form.get('celebrity_id')
        celeb = Celebrity.query.get(int(celeb_id)) if celeb_id else None

        if celeb:
            celeb.celebrity_name = request.form.get('celebrity_name')
            celeb.category = request.form.get('category')
            celeb.Insta = request.form.get('insta_link')
            celeb.yt = request.form.get('yt_link')
            celeb.twitter = request.form.get('twitter_link')

            # Update profile photo if uploaded
            file = request.files.get('profile_photo')
            if file and file.filename:
                celeb.profile_photo = file.read()

            db.session.commit()
            flash(f"{celeb.celebrity_name} updated successfully!", "success")
        else:
            flash("Please select a valid celebrity.", "warning")

        return redirect(url_for('admin_app.edit_celebrity'))

    return render_template('edit_celebrity.html', celebrities=celebrities)

@admin_app.route('/delete_celebrity', methods=['GET', 'POST'])
def delete_celebrity():

    celebrities = Celebrity.query.all()

    if request.method == 'POST':
        selected_ids = request.form.getlist('selected_celebs')
        if selected_ids:
            for celeb_id in selected_ids:
                celeb = Celebrity.query.get(int(celeb_id))
                if celeb:
                    db.session.delete(celeb)
            db.session.commit()
            flash(f"{len(selected_ids)} celebrity(s) deleted successfully!", "success")
        else:
            flash("No celebrities selected.", "warning")
        return redirect(url_for('admin_app.delete_celebrity'))

    return render_template('delete_celebrity.html', celebrities=celebrities)


@admin_app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    # Fetch all users
    all_users = User.query.all()
    blocked_user_ids = {b.user_id for b in Blocked.query.all()}

    active_users = [u for u in all_users if u.user_id not in blocked_user_ids]
    blocked_users = [u for u in all_users if u.user_id in blocked_user_ids]

    if request.method == 'POST':
        # Block selected users
        block_ids = request.form.getlist('block_users')
        for user_id in block_ids:
            if int(user_id) not in blocked_user_ids:
                new_block = Blocked(user_id=int(user_id))
                db.session.add(new_block)

        # Unblock selected users
        unblock_ids = request.form.getlist('unblock_users')
        for user_id in unblock_ids:
            block_entry = Blocked.query.filter_by(user_id=int(user_id)).first()
            if block_entry:
                db.session.delete(block_entry)

        db.session.commit()
        flash("User statuses updated successfully!", "success")
        return redirect(url_for('admin_app.manage_users'))

    return render_template('manage_users.html', active_users=active_users, blocked_users=blocked_users)


