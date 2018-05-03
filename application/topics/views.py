from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.topics.models import Topic
from application.topics.forms import TopicForm

from application.messages.models import Message
from application.messages.forms import MessageForm

from sqlalchemy.sql import text

import os


def mark_messages_read(messages):
    if os.environ.get("HEROKU"):
        for row in messages:
            message_id = row.id
            user_id = current_user.id
            stmt = text("INSERT INTO views (account_id, message_id)"
                        " VALUES (:user_id, :message_id)"
                        " ON CONFLICT DO NOTHING"
                        ).params(user_id=user_id, message_id=message_id)
            res = db.engine.execute(stmt)
    else:
        for row in messages:
            message_id = row.id
            user_id = current_user.id

            stmt = text("INSERT OR IGNORE INTO views (account_id, message_id)"
                        " VALUES (:user_id, :message_id)"
                        ).params(user_id=user_id, message_id=message_id)
            res = db.engine.execute(stmt)


@app.route("/topics/", methods=["GET"])
def topics_index():
    return render_template("topics/list_newest_topics.html",
                           topics=Topic.query.order_by(
                               Topic.date_created.desc())
                           .limit(5).all())


@app.route("/topics/popular/", methods=["GET"])
def topics_popular():
    return render_template("topics/list_popular_topics.html",
                           topics=Topic.find_most_popular())


@app.route("/topics/sql/", methods=["GET"])
def topics_popular_sql():
    return render_template("topics/list_newest_sql_postgre.html",
                           topics=Topic.find_latest_sql())


@app.route("/topics/all/", methods=["GET"])
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
def topics_get_one(topic_id, page=1):
    per_page = 5

    messages = Message.query.filter_by(topic_id=topic_id, reply_id=None)
    mark_messages_read(messages)

    return render_template("topics/one_topic.html", form=MessageForm(),
                           topic=Topic.query.get(topic_id),
                           messages=messages
                           .paginate(page, per_page, False))


@app.route("/topics/<topic_id>/<int:page>", methods=["GET"])
@login_required(role="ANY")
def topics_get_one_paginated(topic_id, page=1):
    per_page = 5

    messages = Message.query.filter_by(topic_id=topic_id, reply_id=None)
    mark_messages_read(messages)

    return render_template("topics/one_topic.html", form=MessageForm(),
                           topic=Topic.query.get(topic_id),
                           messages=messages
                           .paginate(page, per_page, False))


@app.route("/topics/<topic_id>/edit/", methods=["GET"])
@login_required(role="ADMIN")
def topics_get_for_edit(topic_id):
    topic = Topic.query.get(topic_id)
    return render_template("topics/edit.html", form=TopicForm(title=topic.title),
                           topic=topic)


@app.route("/topics/<topic_id>/edit/", methods=["POST"])
@login_required(role="ADMIN")
def topics_edit(topic_id):
    form = TopicForm(request.form)
    print("HEELLLOOUUUU")
    if not form.validate():
        return render_template("topics/edit.html", form=TopicForm(title=form.title.data),
                               topic=Topic.query.get(topic_id))

    t = Topic.query.get(topic_id)
    t.title = form.title.data

    if current_user.admin:
        db.session.commit()

    return redirect(url_for("topics_index"))


@app.route("/topics/<topic_id>/delete/", methods=["POST"])
@login_required(role="ANY")
def topics_delete(topic_id):
    t = Topic.query.get(topic_id)

    db.session.delete(t)
    db.session().commit()

    return redirect("/")


@app.route("/topics/new/", methods=["POST"])
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
