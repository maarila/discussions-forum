from application import db
from application.models import Base


class Topic(Base):

    title = db.Column(db.String(64), nullable=False)
    creator = db.Column(db.String(144), nullable=False)

    def __init__(self, title):
        self.title = title
        self.creator = "anonymous"
