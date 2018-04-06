from application import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    # nullable=True as for now
    topic = db.Column(db.String(144), nullable=True)
    author = db.Column(db.String(144), nullable=False)
    content = db.Column(db.String(1023), nullable=False)
    # simplistic manual read status info
    read = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)

    def __init__(self, content):
        self.content = content
        self.read = False
        self.author = "anonymous"
