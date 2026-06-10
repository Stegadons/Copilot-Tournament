"""
Autentifikācijas serviss
Atbild par administratoru autentifikāciju un sesiju pārvaldību.

POSMS 2 – realizācijas plāns
"""

from werkzeug.security import check_password_hash
from functools import wraps
from flask import session, redirect, url_for, current_app


def _get_admins():
    """Atgriež administratoru sarakstu no app.config['ADMINS']"""
    return current_app.config.get('ADMINS', [])


def verify_credentials(username: str, password: str) -> bool:
    """Pārbauda administratora lietotājvārdu un paroli"""
    for admin in _get_admins():
        if admin.get('username') == username:
            return check_password_hash(admin.get('password_hash'), password)
    return False


def login_user(username: str):
    """Saglabā administratoru sesijā"""
    session['admin_user'] = username


def logout_user():
    """Izņem administratoru no sesijas"""
    session.pop('admin_user', None)


def is_authenticated() -> bool:
    """Pārbauda autentifikācijas statusu"""
    return 'admin_user' in session


def login_required(view_func):
    """Dekorators admin maršrutu aizsardzībai"""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('admin_login'))
        return view_func(*args, **kwargs)
    return wrapper
