from flask import render_template
import requests, os
from threading import Thread
from flask_mail import Message
from flask_babel import _
import requests
from  sqlalchemy.sql.expression import func, select

from app import app, db, mail


def select_by_random():
    if os.environ.get('DATABASE_URL') is None:
        return func.random()
    else:
        return func.rand()

def return_eq_da(symbol):
    for devise in app.config['DEVISES']:
        if devise['symbol'] == symbol:
            return devise['eq_da']

# Google login
def get_google_provider_cfg(discovery_url):
    return requests.get(discovery_url).json()

# Google storage cloud
def allowed_image(filename):
    if not "." in filename:
        return False 
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

# Flask mail sender
def send_async_email(self, app, msg):
    with app.app_context():
        try:
            if app.config['USE_EMAIL_API']:
                headers = {
                    "x-rapidapi-key": current_app.config['RAPIDAPI_KEY'],
                    "x-rapidapi-host": current_app.config['FIREBASE_MAILER_URL'],
                    "Content-Type": "application/json"
                }
                url = "https://send-mail-serverless.p.rapidapi.com/send"
                response = requests.post(url, json=msg, headers=headers)
                print(response.json())
            else:  
                mail.send(msg)
        except Exception as e:
            print(e)

def send_email(subject, sender, recipients, text_body, html_body):
    if app.config['USE_EMAIL_API']:
        for receiver in recipients:
            msg = {
                "personalizations": [
                    { 
                    "to": [
                            {
                                "email": receiver,
                                "name": receiver
                            }
                        ] 
                    }
                ],
                "from": {
                    "email": app.config['SENDER_EMAIL'],
                    "name": app.config['SENDER_NAME']
                },
                "reply_to": {
                    "email": app.config['REPLY_TO_EMAIL'],
                    "name": app.config['SENDER_NAME']
                },
                "subject": subject,
                "content": [
                    {
                        "type": "text/html",
                        "value": html_body
                    },
                    {
                        "type": "text/plan",
                        "value": "Hello You!"
                    }
                ],
                "headers": { "List-Unsubscribe": "<mailto: unsubscribe@firebese.com?subject=unsubscribe>, <https://firebese.com/unsubscribe/id>" }
            }

            Thread(target=send_async_email, args=(app, msg)).start()
        
    else:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        Thread(target=send_async_email, args=(app, msg)).start()

def password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[TRADRDV] Réinitialisez votre mot de passe'),
               sender=app.config['SENDER_EMAIL'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))

def email_confirm_email(user):
    token = user.get_confirm_email_token()
    send_email(_('[TRADRDV] Confirmez votre adresse mail'),
               sender=app.config['SENDER_EMAIL'],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt', user=user, token=token),
               html_body=render_template('email/confirm_email.html', user=user, token=token))

def alert_email(subject, body, url, user):
    send_email('[TRADRDV] '+subject,
               sender=app.config['SENDER_EMAIL'],
               recipients=[user.email],
               text_body=render_template('email/info_email.txt', body=body, url=url, user=user),
               html_body=render_template('email/info_email.html', body=body, url=url, user=user))

def newsletter_email(emails, subject, body, url, username=''):
    send_email('[TRADRDV] '+subject,
               sender=app.config['SENDER_EMAIL'],
               recipients=emails,
               text_body=render_template('email/contact_email.txt', body=body, url=url, username=username),
               html_body=render_template('email/contact_email.html', body=body, url=url, username=username))

