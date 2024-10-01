from flask import Flask, request, g, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
import logging, os
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, _
from flask_babel import lazy_gettext as _l 
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.session_protection = "strong"
client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])
login.login_view = 'login'
login.login_message = _l('Veuillez vous connecter pour accéder à cette page.')
mail = Mail(app)
moment = Moment(app)
scheduler = APScheduler()
scheduler.init_app(app)

def get_locale():
    return getattr(g, 'locale', request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']))
babel = Babel(app, locale_selector=get_locale)



from app import routes, models

@app.cli.command("init_db")
def init_db():
    models.init_db()

@app.cli.command("reinit_admin")
def reinit_admin():
    models.reinit_admin()

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='TRADRDV Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/tradrdv.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Tradrdv startup')
