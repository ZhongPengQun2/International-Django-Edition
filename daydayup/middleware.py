# coding: utf-8
import functools
from flask import request, g, current_app, redirect, g, session
from models.user import User

def access_verify(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("current_user_id", None):
            session["next"] = request.full_path
            return redirect('/login')
        return view(*args, **kwargs)
    return wrapped_view
