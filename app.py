import os

from flask import Flask, request, render_template
from data import TwitterMain
from TweetForm import TweetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
title = 'Twitter Sentiment Analyser'


@app.route('/')
def my_form():
    form = TweetForm(request.form)
    return render_template('index.html', title=title, form=form)


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['search_key']
    count = int(request.form['tweet_count'])
    twit_main = TwitterMain()
    tweets = twit_main.get_trends(text, count)
    return render_template('disp.html', title=title, search_key=text, render_list=tweets)


@app.route('/analysis/<key>')
def analysis(key):
    data = TwitterMain.get_analysis_data(key)
    return render_template('analysis.html', title=title, search_key=key, data=data)


if __name__ == "__main__":
    app.run(debug=True)
