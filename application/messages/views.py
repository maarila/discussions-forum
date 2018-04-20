from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.messages.models import Message
from application.messages.forms import MessageForm


@app.route("/messages/", methods=["GET"])
def messages_index():
    return render_template("messages/list.html", messages=Message.query.all())


@app.route("/messages/<message_id>/", methods=["GET"])
@login_required
def messages_read_one(message_id):
    return render_template("messages/one.html", message=Message.query.get(message_id))


@app.route("/messages/<message_id>/delete/", methods=["POST"])
@login_required
def messages_delete(message_id):
    m = Message.query.get(message_id)

    if current_user.admin:
        db.session.delete(m)
        db.session().commit()

    return redirect(url_for("messages_index"))


@app.route("/topics/<topic_id>/messages/new", methods=["POST"])
@login_required
def messages_create(topic_id):
    form = MessageForm(request.form)

    if not form.validate():
        return render_template("messages/new.html", form=form)

    m = Message(form.name.data)
    m.account_id = current_user.id
    m.topic_id = topic_id

    db.session().add(m)
    db.session().commit()

    return redirect("/topics/" + topic_id + "/")
