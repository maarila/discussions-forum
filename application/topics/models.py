from datetime import datetime

from application import db
from application.models import Base

from sqlalchemy.sql import text


def reduce_msg(message):
    if len(message) < 35:
        return message

    new_msg = ""
    for i in range(32):
        new_msg += message[i]

    new_msg += "..."
    return new_msg


class Topic(Base):

    title = db.Column(db.String(64), nullable=False)
    creator = db.Column(db.String(144), nullable=False)

    def __init__(self, title):
        self.title = title

    @staticmethod
    def find_most_popular():
        stmt = text("SELECT Topic.id, Topic.title, COUNT(Message.id) as msgs FROM Topic"
                    " INNER JOIN Message ON Topic.id = Message.topic_id"
                    " GROUP BY Topic.id"
                    " ORDER BY msgs DESC"
                    " LIMIT 5")
        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"id": row[0], "title": row[1], "msgs": row[2]})

        return response

    @staticmethod
    def find_latest():
        stmt = text("SELECT Topic.id, Topic.title, Message.id, Message.content, Message.date_created FROM Topic"
                    " INNER JOIN Message ON Topic.id = Message.topic_id"
                    " GROUP BY Topic.id"
                    " ORDER BY Message.date_created DESC"
                    " LIMIT 5")
        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"topic_id": row[0], "topic_title": row[1], "msg_id": row[
                            2], "msg_content": reduce_msg(row[3]), "msg_created": datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %-H:%M')})

        return response
