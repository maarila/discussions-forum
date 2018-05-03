from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.auth.models import User
from application.messages.models import Message
from application.topics.models import Topic


@app.route("/users/", methods=["GET"])
@login_required
def users_index():
    return render_template("users/list_users.html", users=User.query.all())


@app.route("/users/<user_id>/", methods=["GET"])
@login_required
def users_get_one(user_id):
    message_count = Message.message_count(user_id)
    latest = Message.find_latest(user_id)
    return render_template("users/one_user.html", count=message_count,
                           latest=latest, user=User.query.get(user_id))


@app.route("/users/<user_id>/", methods=["POST"])
@login_required
def users_set_admin(user_id):
    u = User.query.get(user_id)
    u.admin = not u.admin
    db.session().commit()

    return redirect(url_for("users_index"))


@app.route("/users/<user_id>/delete/", methods=["POST"])
@login_required
def users_delete(user_id):
    Message.query.filter_by(account_id=user_id).delete()
    u = User.query.get(user_id)

    db.session.delete(u)
    db.session().commit()

    return redirect(url_for("users_index"))
