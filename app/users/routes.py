

from app import bcrypt, db
from app.models import User
from app.users.forms import (LoginForm, RegistrationForm, ResetPasswordForm,
                             ResetPasswordRequestForm, UpdateAccountForm)
from app.users.utils import save_picture
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

#from app.users.email import send_password_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(
            f"Account successfuly created for {form.username.data}", "success")

        return redirect(url_for('users.login'))

    return render_template('register.html', form=form, nonav=True)


@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            # this route when user was redirected from a page to login
            # we are sending the user back to that page
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form, nonav=True)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # return file name
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Your account has been updated!', 'success')

        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    #image_file = current_user.get_avatar()
    # print(image_file)

    return render_template('account.html', title=current_user.username, nonav=True, form=form)


""" @users.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print('User Requesting password rest exists .')
            send_password_reset_email(user)
            print('Email Sent to user .')

        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('users.login'))

    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@users.route('/reset-password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('users.login'))
    
    return render_template('reset_password.html', form=form)
 """
""" 
@users.route('/user/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user).order_by(
        Post.date_created.desc()).paginate(per_page=5, page=page)

    return render_template('user_posts.html', user=user, posts=posts) """
