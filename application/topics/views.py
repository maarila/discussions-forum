from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.topics.models import Topic
from application.topics.forms import TopicForm

from application.messages.models import Message
from application.messages.forms import MessageForm


@app.route("/topics/", methods=["GET"])
def topics_index():
    return render_template("topics/list_topics.html", topics=Topic.query.all())


@app.route("/topics/new/", methods=["GET"])
@login_required
def topics_form():
    return render_template("topics/new_topic.html", form=TopicForm())


@app.route("/topics/<topic_id>/", methods=["GET"])
@login_required
def topics_get_one(topic_id):
    return render_template("topics/one_topic.html", form=MessageForm(),
                           topic=Topic.query.get(topic_id),
                           messages=Message.find_messages_in_topic(topic_id))


@app.route("/topics/<topic_id>/delete/", methods=["POST"])
@login_required
def topics_delete(topic_id):
    t = Topic.query.get(topic_id)

    db.session.delete(t)
    db.session().commit()

    return redirect("/")


@app.route("/topics/new", methods=["POST"])
@login_required
def topics_create():
    form = TopicForm(request.form)

    if not form.validate():
        return render_template("topics/new_topic.html", form=form)

    t = Topic(form.title.data)

    db.session().add(t)
    db.session().commit()

    return redirect("/")