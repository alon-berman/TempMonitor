import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_table import Table, Col, LinkCol
from flask import *


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def set_first_admin():
    username = "Amit Steinberg".title()
    mail_address = "Amit.Steinberg@vayyar.com"
    phone_number = "0547982982"
    car_number = "01530153"
    set_admin_flag = True

    db = get_db()
    db.execute(
        'INSERT INTO {} (username, mail_address, phone_number, car_number, qualification)'
        ' VALUES (?, ?, ?, ?, ?)'.format(DB_TABLE_NAME),
        (username, mail_address, phone_number, car_number, set_admin_flag))
    db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    set_first_admin()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


#
# @app.route('/item/<int:id>', methods=['GET', 'POST'])
# def edit(id):
#     qry = db_session.query(db).filter(
#         db.id == id)
#     album = qry.first()
#
#     if album:
#         form = AlbumForm(formdata=request.form, obj=album)
#         if request.method == 'POST' and form.validate():
#             # save edits
#             save_changes(album, form)
#             flash('Album updated successfully!')
#             return redirect('/')
#         return render_template('edit_album.html', form=form)
#     else:
#         return 'Error loading #{id}'.format(id=id)
