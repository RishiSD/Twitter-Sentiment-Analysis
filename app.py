import os

from flask import Flask, request, render_template
from data import TwitterMain

app = Flask(__name__)

from db import db

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def my_form():
    return render_template('myform.html', title='Twitter Sentiment Analysis')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    twit_main = TwitterMain()
    tweets = twit_main.get_trends(text)
    return render_template('disp.html', title='Twitter Sentiment Analysis',search_text=text, render_list=tweets)


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
