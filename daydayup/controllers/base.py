# coding: utf-8
from flask import Blueprint, render_template, request, g, session, redirect
from sqlalchemy.sql import exists
from middleware import access_verify
from models.user import User
from models import db

bp = Blueprint("base", __name__)


@bp.route("/")
@access_verify
def index():
    if request.method == 'GET':
        return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        current_user = User.query.filter_by(username=username, password=password).first()

        if  current_user:
            print "---------------xx", session.get("next", "/")
            session['current_user_id'] = current_user.id
            return redirect(session.get("next", "/"))
        else:
            return render_template("login.html", message=u'用户名或密码错误！')


@bp.route("/logout")
def logout():
    if request.method == 'GET':
       session["current_user_id"] = None
       return redirect("/login")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        if password != repassword:
            return render_template("register.html", message=u"2次密码不相同！")

        user = User(username=username, password=password)
        user.save()

        return redirect("/")