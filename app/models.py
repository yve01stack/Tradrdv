from email.policy import default
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from datetime import datetime, timedelta
import logging as lg

from app import db, login, app, moment


class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    pseudo_com = db.Column(db.String(32), index=True)
    link_com = db.Column(db.String(500), index=True)
    username = db.Column(db.String(32), index=True, unique=True)
    fullname = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(16), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    statut = db.Column(db.String(16), default='client')
    ad_statut = db.Column(db.Boolean, nullable=False, default=False)
    offre_statut = db.Column(db.String(16), default='gratuit')
    offre_begin = db.Column(db.DateTime, default=datetime.utcnow)
    offre_end = db.Column(db.DateTime, default=datetime.utcnow)
    daily_offer = db.Column(db.Integer, default=1)
    remain_day = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String(500), default="https://storage.googleapis.com/tradrdv/dev/OOjs_UI_icon_userAvatar.svg.png")
    country = db.Column(db.String(32), index=True)
    revenu = db.Column(db.Integer, nullable=False, default=0)
    confirmed = db.Column(db.Boolean, default=False)
    google_login = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    traducteurs = db.relationship('Traducteur', backref='author', lazy='dynamic')
    payments = db.relationship('Payment', backref='owner', lazy='dynamic')
    commercials = db.relationship('Commercial', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    contacts = db.relationship('Contact', backref='author', lazy='dynamic')
    chats = db.relationship('Chat', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')

    def as_dict(self):
        return {'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'email': self.email,
            'avatar': self.avatar,
            'country': self.country,
            'last_seen': self.last_seen.strftime("%m/%d/%Y, %H:%M"),
            'timestamp': self.timestamp.strftime("%m/%d/%Y, %H:%M"),
            'is_active': "True" if self.is_active else "False"
            }

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_confirm_email_token(self, expires_in=600):
        return jwt.encode(
            {'confirm_email': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_confirm_email_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['confirm_email']
        except:
            return
        return User.query.get(id)
    
    def set_confirmed(self, confirmed):
        self.confirmed = confirmed

    def has_valid_abon(self):
        remain_day = (self.offre_end - datetime.utcnow()).days
        self.remain_day = remain_day if remain_day >=0 else 0
        self.daily_offer=1
        if remain_day <=0 :
            self.offre_statut = 'gratuit'
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Traducteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispo = db.Column(db.Boolean, nullable=False, default=True)
    accept_subscriber = db.Column(db.Boolean, nullable=False, default=True)
    CCP_number = db.Column(db.String(64))
    BaridiMob_RIP = db.Column(db.String(64))
    ePayment_type = db.Column(db.String(32))
    ePayment = db.Column(db.String(64))
    id_card = db.Column(db.String(500), default="https://storage.googleapis.com/tradrdv/dev/88591.png")
    diploma = db.Column(db.String(500), default="https://storage.googleapis.com/tradrdv/dev/diploma.pdf")
    about_me = db.Column(db.String(500))
    prestation = db.Column(db.String(32), nullable=False, default='Traduction')
    prestation_2 = db.Column(db.String(32))
    prestation_3 = db.Column(db.String(32))
    prestation_4 = db.Column(db.String(32))
    prestation_5 = db.Column(db.String(32))
    prestation_6 = db.Column(db.String(32))
    prestation_7 = db.Column(db.String(32))
    phone = db.Column(db.String(32), nullable=False)
    addr_postale = db.Column(db.String(64), nullable=False)
    caution_annual_begin = db.Column(db.DateTime, default=datetime.utcnow)
    caution_annual_end = db.Column(db.DateTime, default=datetime.utcnow)
    remain_day = db.Column(db.Integer, default=0)
    test_score = db.Column(db.Integer, nullable=False, default=0)
    success_work = db.Column(db.Integer, nullable=False, default=0)
    unsuccess_work = db.Column(db.Integer, nullable=False, default=0)
    skill_1 = db.Column(db.String(64), nullable=False)
    skill_2 = db.Column(db.String(64))
    skill_3 = db.Column(db.String(64))
    skill_4 = db.Column(db.String(64))
    skill_5 = db.Column(db.String(64))
    skill_6 = db.Column(db.String(64))
    skill_7 = db.Column(db.String(64))
    skill_8 = db.Column(db.String(64))
    skill_9 = db.Column(db.String(64))
    skill_10 = db.Column(db.String(64))
    current_country = db.Column(db.String(64), index=True)
    current_town = db.Column(db.String(32))
    compte_valid = db.Column(db.Boolean, nullable=False, default=False)
    need_help_ad = db.Column(db.String(16), default='off') #other value 'off', 'on', 'ask'
    profile_view = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Traducteur {}>'.format(self.skill_1)
    
    def has_valid_abon(self):
        remain_day = (self.caution_annual_end - datetime.utcnow()).days
        self.remain_day = remain_day if remain_day >=0 else 0
        if remain_day <=0 :
            self.compte_valid = False
        db.session.commit()
    
    def add_view(self):
        self.profile_view += 1
        db.session.commit()


    def as_dict(self):
        return {'id': self.id,
            'about_me': self.about_me,
            'prestation': self.prestation,
            'addr_postale': self.addr_postale,
            'success_work': self.success_work,
            'current_country': self.current_country,
            'current_town': self.current_town,
            'skill_1': self.skill_1,
            'skill_2': self.skill_2,
            'skill_3': self.skill_3,
            'skill_4': self.skill_4,
            'skill_5': self.skill_5,
            'skill_6': self.skill_6,
            'skill_7': self.skill_7,
            'skill_8': self.skill_8,
            'skill_9': self.skill_9,
            'skill_10': self.skill_10,
            'author': User.query.filter_by(id=self.user_id).first().as_dict()
            }

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    motif = db.Column(db.String(100), index=True, nullable=False)
    type_deal = db.Column(db.String(16), nullable=False)
    payment_way = db.Column(db.String(16)) #cash, abonnement
    devise = db.Column(db.String(16))
    amount = db.Column(db.Integer, nullable=False, default=0)
    friend_accept = db.Column(db.Boolean, nullable=False, default=False)
    friend_reject = db.Column(db.Boolean, nullable=False, default=False)
    payment_bill = db.Column(db.String(500), default="https://storage.googleapis.com/tradrdv/dev/101671.png")
    bill_is_added = db.Column(db.Boolean, nullable=False, default=False)
    admin_confirm_bill = db.Column(db.Boolean, nullable=False, default=False)
    work_did = db.Column(db.String(500))
    work_valid = db.Column(db.String(500))
    work_score = db.Column(db.Integer, default=0)
    deal_over = db.Column(db.Boolean, nullable=False, default=False)
    deal_over_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship("User", foreign_keys=[user_id])
    friend = db.relationship("User", foreign_keys=[friend_id])

    def __repr__(self):
        return '<Deal {}>'.format(self.amount)


class Commercial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CCP_number = db.Column(db.String(64))
    BaridiMob_RIP = db.Column(db.String(64))
    ePayment_type = db.Column(db.String(32))
    e_Payment = db.Column(db.String(64))
    id_card = db.Column(db.String(500), default="https://storage.googleapis.com/tradrdv/dev/88591.png")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Commercial {}>'.format(self.user_id)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    motif = db.Column(db.String(100), index=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    devise = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Payment {}>'.format(self.amount)
    
def make_payment(motif, amount, devise, eq_da, owner):
    if amount > 0:
        owner.revenu += amount*eq_da
    db.session.add(Payment(motif=motif, amount=amount, devise=devise, owner=owner))
    db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trad_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    avis = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.score)


class Contact(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    receiver_id = db.Column(db.Integer, index=True, nullable=False)
    message = db.Column(db.String(1000))
    file = db.Column(db.String(500))
    file_statut = db.Column(db.Boolean, default=False)
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Contact {}>'.format(self.file_statut)
    
    def as_dict(self):
        return { 'id': self.id,
            'receiver_id': self.receiver_id,
            'message': self.message,
            'file': self.file,
            'file_statut': 'True' if self.file_statut else 'False',
            'read': 'True' if self.read else 'False',
            'timestamp': self.timestamp.strftime("%m/%d/%Y, %H:%M"),
            'author': User.query.filter_by(id=self.user_id).first().as_dict()
        }

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.Integer, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_chat = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Chat {}>'.format(self.last_chat)

    def as_dict(self):
        return {'id': self.id,
            'receiver_id': self.receiver_id,
            'author': User.query.filter_by(id=self.user_id).first().as_dict(),
            'receiver': User.query.filter_by(id=self.receiver_id).first().as_dict(),
            'last_chat': self.last_chat
        }

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Newsletter {}>'.format(self.email)


class Dashbord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    revenu_abon = db.Column(db.Integer, nullable=False, default=0)
    revenu_test = db.Column(db.Integer, nullable=False, default=0)
    revenu_work = db.Column(db.Integer, nullable=False, default=0)
    freelance_part = db.Column(db.Integer, nullable=False, default=0)
    revenu_total = db.Column(db.Integer, nullable=False, default=0)
    accueil_view = db.Column(db.Integer, nullable=False, default=0)
    traducteur_view = db.Column(db.Integer, nullable=False, default=0)
    remain_day = db.Column(db.Integer, default=0)
    begin = db.Column(db.DateTime, default=datetime.utcnow)
    end = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Dashbord {}>'.format(self.id)
    
    def end_valid_month(self):
        remain_day = (self.end - datetime.utcnow()).days
        self.remain_day = remain_day if remain_day >=0 else 0
        if remain_day <=0 :
            last_month = Dashbord.query.filter_by(id=2).first()
            last_month.revenu_abon = self.revenu_abon
            last_month.revenu_test = self.revenu_test
            last_month.revenu_work = self.revenu_work
            last_month.freelance_part = self.freelance_part
            last_month.revenu_total = self.revenu_total
            last_month.accueil_view = self.accueil_view
            last_month.traducteur_view = self.traducteur_view
            last_month.remain_day = self.remain_day
            last_month.begin = self.begin
            last_month.end = self.end

            self.revenu_abon = 0
            self.revenu_test = 0
            self.revenu_work = 0
            self.freelance_part = 0
            self.revenu_total = 0
            self.accueil_view = 0
            self.traducteur_view = 0
            self.remain_day = 0
            self.begin = datetime.utcnow()
            self.end = datetime.utcnow() + timedelta(days=30)
        db.session.commit()

    def update_dashbord(self, revenu_abon=0, revenu_test=0, revenu_work=0, freelance_part=0, eq_da=1, accueil_view=0, traducteur_view=0):
        self.revenu_abon += revenu_abon*eq_da
        self.revenu_test += revenu_test*eq_da
        self.revenu_work += revenu_work*eq_da
        self.freelance_part += freelance_part*eq_da
        self.revenu_total = self.revenu_abon + self.revenu_test + self.revenu_work
        self.accueil_view += accueil_view
        self.traducteur_view += traducteur_view
        db.session.commit()




#database initialized
def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(User(username=app.config['ADMIN_USERNAME'], email=app.config['ADMIN_EMAIL'], country='Algérie (arabe)', fullname=app.config['ADMIN_FULLNAME'], password_hash=app.config['ADMIN_PASSWORD'], statut='admin', confirmed=True))
    db.session.add(User(username=app.config['TESTEUR_USERNAME'], email=app.config['TESTEUR_EMAIL'], country='Algérie (arabe)', fullname=app.config['TESTEUR_FULLNAME'], password_hash=app.config['TESTEUR_PASSWORD'], statut='testeur', confirmed=True))

    new_user = User.query.filter_by(id=2).first()
    traducteur = Traducteur(skill_1='Arabe-français', skill_2='Arabe-anglais', skill_3='', skill_4='', skill_5='', skill_6='', skill_7='', skill_8='', skill_9='', skill_10='',
        phone='+213 658489196', addr_postale='42000, Tipaza, Algérie', caution_annual_end=datetime.utcnow()+timedelta(days=365), compte_valid=True, current_country='Algérie (arabe)', 
        current_town='Tipaza', test_score=4, about_me="Je suis traductrice professionnelle depuis plus de 5ans maintemant, je suis à votre dispotion. Engagez moi!", author=new_user)
    db.session.add(traducteur)

    db.session.add(Dashbord(begin=datetime.utcnow(), end = datetime.utcnow() + timedelta(days=30)))
    db.session.add(Dashbord())

    db.session.commit()
    lg.warning('Database initialized!')

def reinit_admin():
    user = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
    if user:
        user.username = app.config['ADMIN_USERNAME']
        user.fullname = app.config['ADMIN_FULLNAME']
        user.password_hash = app.config['ADMIN_PASSWORD']
        user.statut = 'admin'
        db.session.commit()
        lg.warning('Database admin reinit email: '+user.email)
