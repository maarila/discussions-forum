from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.auth.models import User
from application.messages.models import Message
from application.topics.models import Topic
from application.service.methods import delete_message


@app.route("/users/", methods=["GET"])
@login_required
def users_index():
    return render_template("users/list_users.html", users=User.query.order_by(User.name).all())


@app.route("/users/<user_id>/", methods=["GET"])
@login_required
def users_get_one(user_id):
    message_count = Message.message_count(user_id)
    latest = Message.find_latest(user_id)
    return render_template("users/one_user.html", count=message_count,
                           latest=latest, user=User.query.get(user_id))


@app.route("/users/<user_id>/", methods=["POST"])
@login_required
def users_toggle_admin(user_id):
    u = User.query.get(user_id)

    if current_user.admin and current_user.id != u.id:
        u.admin = not u.admin
        db.session.commit()

    return redirect(url_for("users_index"))


@app.route("/users/<user_id>/delete/", methods=["POST"])
@login_required
def users_delete(user_id):
    users_messages = Message.query.filter_by(account_id=user_id)

    for msg in users_messages:
        delete_message(msg)

    u = User.query.get(user_id)

    if current_user.admin and current_user.id != u.id:
        db.session.delete(u)
        db.session.commit()

    return redirect(url_for("users_index"))
