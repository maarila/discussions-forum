from datetime import datetime

from application import db
from application.models import Base
from application.auth.models import User

from sqlalchemy.sql import text


views = db.Table('views',
                 db.Column('account_id', db.Integer, db.ForeignKey(
                     'account.id'), primary_key=True),
                 db.Column('message_id', db.Integer, db.ForeignKey(
                     'message.id'), primary_key=True)
                 )


class Message(Base):
    author = db.Column(db.String(144), nullable=True)
    content = db.Column(db.String(1023), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'),
                         nullable=False)

    reply_id = db.Column(db.Integer, db.ForeignKey(
            'message.id'), nullable=True)

    views = db.relationship('User', secondary=views, lazy='subquery',
                            backref=db.backref('message', lazy=True))

    def __init__(self, content):
        self.content = content
        self.read = False

    @staticmethod
    def find_messages_by_date(start, end):
        end_of_day = end + " 23:59:59"

        stmt = text("SELECT * FROM Message"
                    " WHERE date_created BETWEEN :start AND :end"
                    ).params(start=start, end=end_of_day)

        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"id": row[0], "date_created": datetime.strptime(
                row[1], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %-H:%M'),
                "author": row[3], "content": row[4], "topic_id": row[7]})

        return response
