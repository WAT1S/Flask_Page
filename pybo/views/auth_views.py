from flask import Blueprint, g, render_template, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .. import db
from ..models import User
from ..forms import UserCreateForm, UserLoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/auth/", methods=("POST","GET"))
def signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            user_id = session.get("user_id")
            g.user = User.query.get(user_id)
            return redirect(url_for("main.index"))
        else:
            flash("Account already exists")
    return render_template("auth/signup.html", form=form)

@bp.route("/login/", methods=("POST","GET"))
def login():
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.index"))
        flash(error)
    return render_template("auth/login.html", form=form)
    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        
@bp.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("main.index"))