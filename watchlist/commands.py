import click
from watchlist import app, db
from watchlist.models import User, Movie

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


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to loging')
def admin(username, password):
    # Create user.
    db.create_all()
    user = User.query.filter_by(username=username).first()

    if user is not None:
        click.echo('Updating user ...')
        # 数据写不进去是因为原来配置的是 user.name = username
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name=username)
        user.set_password(password)
        db.session.add(user)
        
    db.session.commit()
    click.echo('Done.')