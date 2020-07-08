import sqlite3

import click
import requests
from math import ceil
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def init_db():
    import properties.models

    db.create_all()


def drop_db():
    db.drop_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""

    init_db()
    click.echo("Initialized the database.")


@click.command("drop-db")
@with_appcontext
def drop_db_command():
    """Clear the existing data and drop all tables."""
    drop_db()
    click.echo("Database Droped.")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
    db.init_app(app)