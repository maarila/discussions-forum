from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.topics.models import Topic
from application.topics.forms import TopicForm

from application.messages.models import Message
from application.messages.forms import MessageForm


@app.route("/topics/", methods=["GET"])
def topics_index():
    return render_template("topics/list_topics.html",
                           topics=Topic.query.order_by(
                               Topic.date_created.desc())
                           .limit(5).all())


@app.route("/topics/popular", methods=["GET"])
def topics_popular():
    return render_template("topics/list_popular_topics.html",
                           topics=Topic.find_most_popular())


@app.route("/topics/all", methods=["GET"])
def topics_all():
    return render_template("topics/list_all_topics.html",
                           topics=Topic.query.order_by(
                               Topic.date_created.desc()).all())


@app.route("/topics/new/", methods=["GET"])
@login_required(role="ADMIN")
def topics_form():
    return render_template("topics/new_topic.html", form=TopicForm())


@app.route("/topics/<topic_id>/", methods=["GET"])
@login_required(role="ANY")
def topics_get_one(topic_id):
    return render_template("topics/one_topic.html", form=MessageForm(),
                           topic=Topic.query.get(topic_id),
                           messages=Message.query.filter_by(topic_id=topic_id).all())


@app.route("/topics/<topic_id>/delete/", methods=["POST"])
@login_required(role="ANY")
def topics_delete(topic_id):
    t = Topic.query.get(topic_id)

    db.session.delete(t)
    db.session().commit()

    return redirect("/")


@app.route("/topics/new", methods=["POST"])
@login_required(role="ADMIN")
def topics_create():
    form = TopicForm(request.form)

    if not form.validate():
        return render_template("topics/new_topic.html", form=form)

    t = Topic(form.title.data)
    t.creator = current_user.name

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("topics_index"))
