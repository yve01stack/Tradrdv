from flask_babel import lazy_gettext as _l
import os, json
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY', None)
	SCHEDULER_API_ENABLED = True
	# Database initialization
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
		SQLALCHEMY_TRACK_MODIFICATIONS = False
	else:
		SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
		SQLALCHEMY_TRACK_MODIFICATIONS = True

	ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", None) 
	ADMIN_FULLNAME = os.environ.get("ADMIN_FULLNAME", None) 
	ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", None)
	ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", None)
	TESTEUR_USERNAME = os.environ.get("TESTEUR_USERNAME", None) 
	TESTEUR_FULLNAME = os.environ.get("TESTEUR_FULLNAME", None) 
	TESTEUR_EMAIL = os.environ.get("TESTEUR_EMAIL", None)
	TESTEUR_PASSWORD = os.environ.get("TESTEUR_PASSWORD", None)

	f = open(os.path.join('app', 'static', 'data_files', 'static_data.json'), 'r', encoding='utf-8')
	data = json.load(f)
	f.close()

	COUNTRIES = data['countries']
	TOWNS = data['twons']
	SKILLS = data['skills']

	# Site Informations
	SITE_NAME = "TRADRDV"
	SITE_DESCRIPTION = _l("Traducteurs sur Rendez-vous est la première plateforme qui regroupe des traducteurs freelancers algériens, "\
		 "et bientôt des prestataires des quatre coins du monde !")
	SITE_ICONE = os.path.join('assets', 'images', 'dev', 'favicon.png').replace("\\", '/')
	MAIL_CONTACT = 'traducteurs.contactofficiel@gmail.com'
	CALL_CONTACT = '+213 658489196'
	FAX_CONTACT = '---'
	ADDRESS = '42000, Tipasa, Algérie'

	E_PAYMENT_TYPES = ['Payonner', 'Western Union', 'Compte Bancaire']
	STATUTS = ['admin', 'testeur', 'traducteur', 'client']
	NEWSLETTER_GROUPS = ['Groupe particulier', 'Groupe client', 'Groupe traducteur', 'Groupe testeur', 'Groupe admin']
	PRESTATIONS = ['Interprétation', 'Traduction', 'Transcription', 'Relecture', 'Sous-titrage', 'Voix-off', 'Doublage']
	SEX = ['Féminin', 'Masculin']
	PAYMENT_WAY = ['cash', 'abonnement']
	DEVISES = [{'name': 'DZD', 'symbol': 'DA', 'eq_da': 1}, {'name': 'POUND', 'symbol': '£', 'eq_da': 162}, {'name': 'EURO', 'symbol': '€', 'eq_da': 140}, {'name': 'DOLLAR', 'symbol': '$', 'eq_da': 139}]
	PAYMENT_METHOD = [{'name': 'CCP', 'desc': 'GHEDIRI Hanane -  0002054044 clé 96 - adresse : Tipaza'},
		{'name': 'MaridiMob', 'desc': '00799999000205404496'}, {'name': 'Western Union', 'desc': 'Nom: GHEDIRI, Prénom: Hanane, Pays: Algérie, Ville: Tipaza, Code postal: 42000'},
		{'name': 'Payonner', 'desc': 'hananeinterpretingworld@gmail.com'}]
	TRADUCTEUR_CAUTION = {'price_eur': 80.00, 'price_da': 15000}
	OFFRE_STATUTS = {'gratuit':{'price_eur': 0.0, 'price_da': 0}, 'standard':{'price_eur': 55.00, 'price_da': 7500}, 'premium':{'price_eur': 80.00, 'price_da': 11000}}
	COVER_PICTURE = os.path.join('assets', 'images', 'dev', 'OOjs_UI_icon_userAvatar.svg.png').replace("\\", '/')
	ORDER_PER_PAGE = 20
	PUB_CATEGORIES = ['Sport', 'Produit', 'Cuisine']

	# freelancer payment
	TESTEUR_PART = 2500
	TRAD_PART_ABON = 200
	TRAD_PART_NO_ABON = 80 #%
	DONATION_PART = 2 #%
	IMPOT_PART = 5 #%

	# Google config
	GOOGLE_CLIENT_ID =  os.environ.get("GOOGLE_CLIENT_ID", None)
	GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
	GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
	SOCIAL_LOGIN_PWD = os.environ.get('SOCIAL_LOGIN_PWD', None)
	RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", None)
	RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", None) 
	CLOUD_STORAGE_BUCKET = 'tradrdv'
	# Verify picture download
	ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF", "SVG", "JFIF"]
	MAX_IMAGE_FILESIZE = 3 * 1024 * 1024
	
	# flask mail sender
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_PORT = 25
	MAIL_USE_TLS = 1
	
	USE_EMAIL_API = True
	SENDER_NAME = "TRADRDV" 
	SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
	REPLY_TO_EMAIL = os.environ.get('REPLY_TO_EMAIL')
	ALIEXPRESS_URL = os.environ.get('ALIEXPRESS_URL')
	RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
	FIREBASE_MAILER_URL = os.environ.get('FIREBASE_MAILER_URL')

	ADMINS = ['contact@tradrdv.com', 'admin@tradrdv.com', 'programm01dev@gmail.com']
	# flask babel translator
	BABEL_DEFAULT_LOCALE = 'fr'
	BABEL_SUPPORTED_LOCALES = ['fr', 'en', 'ar']
