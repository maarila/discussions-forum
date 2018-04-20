from flask import render_template, url_for, redirect
from application import app
from application.topics.models import Topic

@app.route("/")
def index():
    return redirect(url_for("topics_index"))
    