from application import db
from application.models import Base

from sqlalchemy.sql import text


class Topic(Base):

    title = db.Column(db.String(64), nullable=False)
    creator = db.Column(db.String(144), nullable=False)

    def __init__(self, title):
        self.title = title

    @staticmethod
    def find_most_popular():
        stmt = text("SELECT Topic.id, Topic.title, COUNT(Message.id) as msgs FROM Topic"
                    " INNER JOIN Message ON Topic.id = Message.topic_id"
                    " GROUP BY Topic.title"
                    " ORDER BY msgs DESC"
                    " LIMIT 5")
        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"id": row[0], "title": row[1], "msgs": row[2]})

        return response
