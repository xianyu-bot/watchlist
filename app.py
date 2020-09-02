from flask import Flask
from flask import url_for
from flask import render_template

app = Flask(__name__)

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@app.route('/')
def hello():
    return "Welcome to My firstweb"


@app.route('/index')
def index():
    return render_template('index.html', name=name, movies=movies)
