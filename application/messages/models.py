from application import db
from application.models import Base

from sqlalchemy.sql import text


class Message(Base):

    # viestin tiedot: sisältö, kuka kirjoittanut, kuka lukenut, mihin topicciin liittyy
    author = db.Column(db.String(144), nullable=True)
    content = db.Column(db.String(1023), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'),
                         nullable=False)

    def __init__(self, content):
        self.content = content
        self.read = False
        self.author = "anonymous"


    @staticmethod
    def find_messages_in_topic(topic_id):
        stmt = text("SELECT * FROM Message"
             " WHERE topic_id = :topic_id").params(topic_id=topic_id)
        res = db.engine.execute(stmt)

        return res
