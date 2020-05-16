import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # for sending text-only messages

from flask import (
    Blueprint, flash, g, render_template, request, redirect, url_for
)

from .config import *

from .db import get_db

bp = Blueprint('search', __name__, url_prefix='/')


@bp.route('/search_blocked_user', methods=('GET', 'POST'))
def get_input():
    if not request.form:
        return redirect(url_for('home'))

    db = get_db()
    app_user = db.execute('SELECT * FROM {} WHERE id = ?'.format(DB_TABLE_NAME), (request.cookies.get('VayyarParkingLot'),)).fetchone()

    error = None
    unknown_plate = None
    notify_flag = False

    blocked_car_number = request.form['BlockedCarNum']

    if request.method == 'POST':
        if "goto_login_page" in request.form:
            return redirect(url_for('auth.login'))

        elif "notify" in request.form:
            if blocked_car_number is not '':
                if blocked_car_number == '072012072012':  # Go to DATABASE
                    full_db = db.execute("select * from {}".format(DB_TABLE_NAME)).fetchall()
                    return render_template("database.html", rows=full_db, user=app_user['username'])
                else:
                    blocked_user = db.execute('SELECT * FROM {} WHERE car_number = ?'.format(DB_TABLE_NAME), (blocked_car_number,)
                                              ).fetchone()
                    if not blocked_user:
                        error = append_to_error(error, "The car plate you entered is not registered in the database")
                        unknown_plate = blocked_car_number
                    else:
                        notify_blocked_user(app_user, blocked_user)
                        notify_flag = True
            else:
                error = append_to_error(error, "plz enter a valid car number")
        elif "report_unregistered_car" in request.form:
            if blocked_car_number is not '':
                report_unregistered_car(g.user, blocked_car_number)
            else:
                error = append_to_error(error, "plz enter a valid car number")

    flash(error)

    return render_template('index.html', unknown_plate=unknown_plate, user=app_user['username'],
                           notify_flag=notify_flag)


def report_unregistered_car(reporter, blocked_car_number):
    sending_ts = datetime.now()
    sub = "Unregistered car report %s" % sending_ts.strftime('%Y-%m-%d %H:%M:%S')

    to = get_all_admin_mail()

    body = "Hi Shani" + "\n\n" + "You have a new report from " + reporter["username"] + "\n" + \
           reporter["username"] + " says that the plate number " + str(blocked_car_number) + "is blocked by him" + \
           "\n" + "this report is about an unregistered car" + "\n" + \
           "Please make sure that this car belongs to a Vayyar's employee" + "\n" \
           "the number is " + str(blocked_car_number)

    send_mail(to, sub, body)


def notify_blocked_user(blocking_user, blocked_user):
    sending_ts = datetime.now()
    sub = "your car is being blocked %s" % sending_ts.strftime('%Y-%m-%d %H:%M:%S')

    to = blocked_user['mail_address']

    body = "Hi " + blocked_user['username'] + "\n\n" + "your car is being blocked by " + blocking_user['username'] +\
           "\n" + "if you want to move out first call " + blocking_user['username'] + "\n" + "His Phone number is: " +\
           str(blocking_user['phone_number'])

    send_mail(to, sub, body)


def send_mail(to, sub, body):

    msg = MIMEMultipart('alternative')
    msg['From'] = 'demo.pc+parkinglot@imagintechnology.com'
    msg['To'] = to
    msg['Subject'] = sub

    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 25)
    s.starttls()
    s.login('demo.pc@imagintechnology.com', 'dPC123456!')
    s.send_message(msg)
    s.quit()


@bp.route('/database_view')
def database_view():
    db = get_db()
    full_db = db.execute("select * from {}".format(DB_TABLE_NAME)).fetchall()
    return render_template("database.html", rows=full_db)


def append_to_error(error, msg):
    if error:
        return error + ' and also ' + msg
    return msg


def get_all_admin_mail():
    db = get_db()
    admins_mail = db.execute("""SELECT mail_address FROM {} WHERE qualification = ?""".format(DB_TABLE_NAME), (1,)).fetchall()
    emails = []
    for row in admins_mail:
        emails.append(row[0])
    emails_string = ', '.join(emails)
    return emails_string
