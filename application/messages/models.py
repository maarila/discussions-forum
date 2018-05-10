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
    author = db.Column(db.String(64), nullable=True)
    content = db.Column(db.String(2048), nullable=False)
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

    @staticmethod
    def find_all(search_term):
        searching_for = '%' + search_term + '%'

        stmt = text("SELECT * FROM Message"
                    " WHERE Message.author LIKE :search"
                    " OR Message.content LIKE :search"
                    " ORDER BY Message.date_created DESC"
                    " LIMIT 30").params(search=searching_for)
        res = db.engine.execute(stmt)

        return res

    @staticmethod
    def message_count(user_id):
        stmt = text("SELECT COUNT(*) AS messages FROM Message"
                    " WHERE Message.account_id = :user_id").params(user_id=user_id)
        res = db.engine.execute(stmt)

        count = 0
        for row in res:
            count += row[0]

        return count

    @staticmethod
    def find_latest(user_id):
        stmt = text("SELECT m.id, m.date_created, m.content, m.topic_id, Topic.title FROM Message AS m"
                    " INNER JOIN Topic ON m.topic_id = topic.id"
                    " WHERE m.account_id = :user_id"
                    " ORDER BY m.date_created DESC"
                    " LIMIT 1").params(user_id=user_id)
        res = db.engine.execute(stmt)

        response = {}

        for row in res:
            content = row[2]
            if len(content) > 50:
                content = content[:32] + "..."
            response["id"] = row[0]
            response["date_created"] = row[1]
            response["content"] = content
            response["topic_id"] = row[3]
            response["topic_title"] = row[4]

        return response
