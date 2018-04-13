from flask import render_template
from application import app
from application.topics.models import Topic

@app.route("/")
def index():
    return render_template("/topics/list_topics.html", topics=Topic.query.all())
    