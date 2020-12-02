# flaskr/db.py

import sqlite3

import click
from flask import current_app, g # special object for request
from flask.cli import with_appcontext

def get_db():
    """
    Create a connection to db. Note the db can be nonexist, and be initiated later. 
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    # return a connection to database
    return g.db


def close_db(e=None):
    """
    Check if a connection was created by checking if g.db was set.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """ Database initialization
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Define a command line command called 'init-db' to init db
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Functions need to be registered with the application instance accordingly to be recognized. 
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)