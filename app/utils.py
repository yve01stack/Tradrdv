from flask import render_template
import requests, os
from threading import Thread
from flask_mail import Message
from flask_babel import _
import sendgrid
from sendgrid.helpers.mail import *
from  sqlalchemy.sql.expression import func, select

from app import app, db, mail, storage_client


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
        
def delete_async_img(app, blob):
    with app.app_context():
        blob.delete()

def delete_blob_img(bucket_name, public_url):
    """Deletes a blob from the bucket."""
    bucket = storage_client.bucket(bucket_name)
    if bucket_name in public_url:
        if not '/dev/' in public_url:
            blob_name = public_url.replace("https://storage.googleapis.com/"+bucket_name+"/","")
            blob = bucket.blob(blob_name)
            Thread(target=delete_async_img, args=(app, blob)).start()

def upload_blob_img(bucket_name, uploaded_file, dossier):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(dossier+'/'+uploaded_file.filename)
    #blob.upload_from_string(uploaded_file.read(), content_type=uploaded_file.content_type)
    blob.upload_from_filename(os.path.join('app', 'static', 'assets', 'images' ,'cloud_img', uploaded_file.filename))
    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url

def upload_blob_file(bucket_name, uploaded_file, dossier):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(dossier+'/'+uploaded_file.filename)
    #blob.upload_from_string(uploaded_file.read(), content_type=uploaded_file.content_type)
    blob.upload_from_filename(os.path.join('app', 'static', 'assets', 'images' ,'cloud_file', uploaded_file.filename))
    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url

# Flask mail sender
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    if app.config['SENDGRID_NEED']:
        for receiver in recipients:
            sendgrid_mail(subject, receiver, html_body)
    else:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        Thread(target=send_async_email, args=(app, msg)).start()

def sendgrid_mail(subject, receiver, html_body):
    sg = sendgrid.SendGridAPIClient(api_key=app.config['SENDGRID_KEY'])
    from_email = Email(app.config['EMAIL_SENDER'])
    to_email = To(receiver)
    subject = subject
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[TRADRDV] Réinitialisez votre mot de passe'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))

def email_confirm_email(user):
    token = user.get_confirm_email_token()
    send_email(_('[TRADRDV] Confirmez votre adresse mail'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt', user=user, token=token),
               html_body=render_template('email/confirm_email.html', user=user, token=token))

def alert_email(subject, body, url, user):
    send_email('[TRADRDV] '+subject,
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/info_email.txt', body=body, url=url, user=user),
               html_body=render_template('email/info_email.html', body=body, url=url, user=user))

def newsletter_email(emails, subject, body, url, username=''):
    send_email('[TRADRDV] '+subject,
               sender=app.config['ADMINS'][0],
               recipients=emails,
               text_body=render_template('email/contact_email.txt', body=body, url=url, username=username),
               html_body=render_template('email/contact_email.html', body=body, url=url, username=username))

