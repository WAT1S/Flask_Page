from flask import Blueprint, request, url_for, render_template
from werkzeug.utils import redirect
from ..models import Question
from ..forms import QuestionForm, AnswerForm
from datetime import datetime
from .. import db

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
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Question(subject = form.subject.data, content = form.content.data, create_date = datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("question/question_form.html", form=form)