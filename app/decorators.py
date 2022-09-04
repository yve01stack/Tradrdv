from functools import wraps

from flask import flash, redirect, url_for, make_response, render_template
from flask_login import current_user
from flask_babel import _


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('confirm_email', _external=True))
        return func(*args, **kwargs)
    return decorated_function

def check_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.statut == 'admin':
            return make_response(render_template("404.html"), 404)
        return func(*args, **kwargs) 
    return decorated_function

def check_manager(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.statut == 'testeur':
            if not current_user.statut == 'traducteur':
                return make_response(render_template("404.html"), 404)
        return func(*args, **kwargs)
    return decorated_function

def in_development(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        in_development = True
        if in_development:
            return make_response(render_template("000.html"), 404)
        return func(*args, **kwargs)
    return decorated_function