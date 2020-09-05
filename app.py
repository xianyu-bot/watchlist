from flask import Flask
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型监控的修改

db = SQLAlchemy(app)

# name = 'Grey Li'
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    db.create_all()

    name = "xianyu"
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo("Insert Done.")


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route('/')
def hello():
    return "Welcome to My firstweb"


@app.route('/index')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)
