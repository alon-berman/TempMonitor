from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)

from db import get_db
from search import send_mail, append_to_error, get_all_admin_mail

from config import *

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM {} WHERE id = ?'.format(DB_TABLE_NAME), (user_id,)).fetchone()


@bp.route('/sign', methods=('GET', 'POST'))
def register():
    # if not request.form:
    #     return redirect(url_for('home'))

    db = get_db()
    app_user = db.execute('SELECT * FROM {} WHERE id = ?'.format(DB_TABLE_NAME), (request.cookies.get('VayyarParkingLot'),)).fetchone()

    reg_msg = None
    url = None
    error = None
    set_admin_flag = None
    is_admin = None

    if app_user:
        is_admin = app_user['qualification']

    if request.method == 'POST' and "signup_page" not in request.form:

        username = request.form["username"].title()
        mail_address = request.form["mail"].lower()
        car_number = request.form["carNumber"]
        phone_number = request.form["phone"]
        phone_number = format_phone_num("05"+phone_number)

        mail_address_for_url = mail_address.replace('@', '%40')
        username_for_url = username.replace(" ", "+")
        url = (request.url +
               '?username=' + username_for_url +
               '&mail=' + mail_address_for_url +
               '&carNumber=' + car_number +
               '&phone=' + phone_number[2:].replace('-', ''))

        if not username or not mail_address or not car_number or not phone_number:
            error = append_to_error(error, 'all the fields required.')

        else:
            new_user = db.execute('SELECT * FROM {} WHERE username = ?'.format(DB_TABLE_NAME), (username,)).fetchone()
            if new_user:
                error = append_to_error(error, 'Did you mean to log in as GIVE CLOSE username.')
            elif not new_user:
                if not mail_address.endswith('@vayyar.com'):
                    error = append_to_error(error, "This Email is not Vayyar's.")

                if error is None:
                    if "send_full_data" in request.form:
                        note_hr_on_new_join_request(username, mail_address, phone_number, car_number, url)
                        reg_msg = "a mail sent to HR, you would be notified when registered"
                        return render_template('signup.html', admin=is_admin, regMSG=reg_msg)

                    elif "user_full_data" in request.form:
                        set_admin_flag = request.form['user_type']
                        db.execute(
                            'INSERT INTO {} (username, mail_address, phone_number, car_number, qualification)'
                            ' VALUES (?, ?, ?, ?, ?)'.format(DB_TABLE_NAME),
                            (username, mail_address, phone_number, car_number, set_admin_flag))
                        db.commit()
                        note_user_success_join(str(username), mail_address, str(app_user['username']))
                        reg_msg = "Thanks for adding {} to the data base, He will be notified".format(username)
                        return render_template('signup.html', admin=is_admin, regMSG=reg_msg)

    flash(error)

    if url:
        return redirect(str(url))
    return render_template('signup.html', admin=is_admin, regMSG=reg_msg)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # if not request.form:
    #     return redirect(url_for('home'))

    db = get_db()

    mail_address = None
    error = None

    if request.method == 'POST':
        mail_address = request.form['mail_address']

        if "signup" in request.form:
            return render_template('signup.html', mail_add=mail_address)

        if mail_address:
            user = db.execute('SELECT * FROM {} WHERE mail_address = ?'.format(DB_TABLE_NAME), (mail_address,)).fetchone()

            if user is None:
                error = append_to_error(error, "Sorry, we can't seem to find you in the data base.")
                return render_template('login.html', un_known_user=mail_address, bad_mail=mail_address)
            if error is None:
                res = make_response(redirect(url_for('home')))
                res.set_cookie('VayyarParkingLot', str(user['id']).encode(), max_age=60 * 60 * 24 * 365 * 2)
                session.clear()
                session['id'] = user['id']
                session['username'] = user['username']
                return res
        elif not mail_address:
            error = append_to_error(error, "Don't forget to enter the mail.....")

    flash(error)

    return render_template('login.html', bad_mail=mail_address)


def note_hr_on_new_join_request(username, mail_address, phone_number, car_number, url):
    to = get_all_admin_mail()

    sub = username + "'s parking lot app registration request"

    body = "Hi Shani" + "\n\n" + "You have a new request to add a user to the parking lot application" + "\n" + \
           "User name: " + username + "\n" + \
           "Email address: " + mail_address + "\n" + \
           "Phone number: " + phone_number + "\n" + \
           "Car plate: " + car_number + "\n\n" + \
           "You can also copy the information from here -" + \
           "\n\n" + url + "\n\n" + \
           "please update " + username + " about the process."

    send_mail(to, sub, body)


def note_user_success_join(username, mail_address, app_user):
    sub = username + "'s successful parking lot app registration request"

    body = "Hi " + username + "\n\n" + "You have been successfully added to the parking lot database" + "\n" + \
           "You can thanks " + app_user + " for it."

    send_mail(mail_address, sub, body)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/edit_user', methods=('GET', 'POST'))
def edit():
    if not request.form:
        return redirect(url_for('home'))

    db = get_db()
    error = None

    if request.method == 'POST':
        if 'Edit' in request.form:
            user_id = request.form['Edit']
            full_db = db.execute("select * from {}".format(DB_TABLE_NAME)).fetchall()
            return render_template('database.html', user_id=user_id, rows=full_db)

        elif 'Save' in request.form:
            # todo: change condition to be an integer instead of list
            is_admin = False
            if 'is_admin' in request.form:
                is_admin = True
            # print(request.form)
            # print(request.form.getlist('Save'))
            db.execute(
                'UPDATE {} '
                'SET '
                # 'mail_address = ?,'
                'phone_number = ?,'
                'car_number = ?,'
                'qualification = ?'
                ' WHERE id = ?'.format(DB_TABLE_NAME), (
                    request.form['phone_number'], request.form['car_number'],
                    is_admin, request.form['Save']))
            db.commit()
            full_db = db.execute("select * from {}".format(DB_TABLE_NAME)).fetchall()
            return render_template('database.html', rows=full_db, user_id="-1")


def format_phone_num(phone_number):
    bad_chars = '+-*/|&.eN" '
    for ch in bad_chars:
        phone_number = phone_number.replace(ch, '')
    phone_number = "{}-{}-{}".format(phone_number[:3], phone_number[3:7], phone_number[7:])
    return phone_number
