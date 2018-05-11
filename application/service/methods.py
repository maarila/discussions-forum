from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.messages.models import Message
from application.messages.forms import MessageForm

from sqlalchemy.sql import text

import os


def delete_topic(topic):
    replies_to_topic = Message.query.filter_by(topic_id=topic.id).all()

    if not replies_to_topic:
        db.session.delete(topic)
        db.session.commit()
    else:
        for msg in replies_to_msg:
            delete_message(msg)

        db.session.delete(topic)
        db.session.commit()


def delete_message(message):
    replies_to_msg = Message.query.filter_by(reply_id=message.id).all()

    if not replies_to_msg:
        db.session.delete(message)
        db.session.commit()
    else:
        for msg in replies_to_msg:
            delete_message(msg)

        db.session.delete(message)
        db.session.commit()


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


def reduce_msg(message):
    if len(message) < 35:
        return message

    new_msg = ""
    for i in range(32):
        new_msg += message[i]

    new_msg += "..."
    return new_msg
