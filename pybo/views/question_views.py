from flask import Blueprint, request, url_for, render_template, g, flash
from werkzeug.utils import redirect
from ..models import Question
from ..forms import QuestionForm, AnswerForm
from datetime import datetime
from .. import db
from .auth_views import login_required

bp = Blueprint("question", __name__, url_prefix="/question")

@bp.route("/list/")
def _list():
    page = request.args.get("page", type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.asc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template("question/question_list.html", question_list = question_list)

@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    return render_template("question/question_detail.html", question=question, form=form)


@bp.route("/create/", methods=("POST", "GET"))
@login_required
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Question(subject = form.subject.data, content = form.content.data, create_date = datetime.now(), user = g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("question/question_form.html", form=form)

@bp.route("/modify/<int:question_id>", methods=("GET", "POST"))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("수정권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=question_id))
    if request.method == "POST":       
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", question_id=question_id))
    else:
        form= QuestionForm(obj=question)
    return render_template("question/question_form.html", form=form)

@bp.route("/delete/<int:question_id>", methods=("GET","POST"))
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("삭제 권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question._list"))


