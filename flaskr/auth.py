# flaskr/auth.py

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# create a blueprint for view associated with register and login
bp = Blueprint('auth', __name__, url_prefix='/auth')

"""The following view functions are registered with a Blueprint object, and Blueprints are registered with the app. """

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        """when user submit the form"""
        
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # insert username password hash to db
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            # redirect to login page
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password): # check the submitted password against the hashed password 
            error = 'Incorrect password.'

        if error is None:
            session.clear() # clear former session
            session['user_id'] = user['id'] # session is a dict stores data across requests, the data is stored in a cookie 
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


"""
before_app_request registers a function that runs before the view function, no matter what URL is requested"""
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

"""authentication also required in other views, ie, views for creating, editing, deleting blog posts"""
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
