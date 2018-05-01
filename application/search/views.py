from flask import render_template, url_for, redirect, request

from application import app
from application.topics.models import Topic
from application.messages.models import Message

from application.search.forms import SearchForm, SearchDateForm


@app.route("/search/", methods=["GET"])
def search_index():
    return render_template("search/search.html", form=SearchForm(),
                           dateform=SearchDateForm())


@app.route("/search/topic/", methods=["POST"])
def search_topic():
    topics = []
    messages = []

    form = SearchForm(request.form)
    search_term = form.search_phrase.data

    if not form.validate():
        return redirect(url_for('search_index'))

    searching_for = form.searching_for.data

    if searching_for == "topic":
        topics = Topic.query.filter(
            Topic.title.like("%" + search_term + "%")).all()
    elif searching_for == "author":
        messages = Message.query.filter(
            Message.author.like("%" + search_term + "%")).all()
    else:
        results = Topic.find_topics_or_messages(search_term)

    return render_template("search/search.html", topics=topics, messages=messages,
                           form=SearchForm(), dateform=SearchDateForm())
