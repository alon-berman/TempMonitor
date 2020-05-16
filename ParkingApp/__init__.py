import os

from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import *
from db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,)
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["1000 per day", "1000 per hour"]
    )
    limiter.init_app(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=r'C:\Vayyar\SW\Imaging\BringUp\AmitSteinberg\ParkingApp\db\parking_app_db.sqlite',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(DB_PATH)
    except OSError:
        pass

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return make_response(
            render_template("rate_limit.html"), 429
        )


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Goodbye, World!'

    @app.route("/")
    def home():
        if device_known():
            # print("----====----===---this is the user id for this session goes to index" + str(session['user_id']))
            # if "goto_signup_page" in request.form:
            #     return render_template("login.html")
            return render_template("index.html", user=g.user['username'])
            # return redirect(url_for('search'))
        else:
            # print("----====----===---this is the user id for this session goes to signup" + str(session['user_id']))
            # return redirect(url_for('sign'))
            return render_template("login.html")
            # return redirect(url_for('login'))

    def device_known():
        # if 'user_id' in session:
        if g.user is not None:
            return True  # check in cache
        else:
            if request.cookies.get('VayyarParkingLot') is not None:
                db = get_db()
                g.user = db.execute(
                    'SELECT * FROM {} WHERE id = ?'.format(DB_TABLE_NAME), (request.cookies.get('VayyarParkingLot'),)
                    ).fetchone()
                return True
            return False

    import db
    db.init_app(app)

    import auth
    app.register_blueprint(auth.bp)

    import search
    app.register_blueprint(search.bp)

    return app


create_app()