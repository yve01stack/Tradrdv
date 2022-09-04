from flask_babel import lazy_gettext as _l
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY', None)
	# Database initialization
	if os.environ.get('DATABASE_URL') is None:
		basedir = os.path.abspath(os.path.dirname(__file__))
		SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
		SQLALCHEMY_TRACK_MODIFICATIONS = False
	else:
		PASSWORD = os.environ.get("GCP_INSTANCE_PWD", None)
		PUBLIC_IP_ADDRESS = os.environ.get("GCP_PUBLIC_IP_ADDRESS", None)
		DBNAME = os.environ.get("GCP_DB_NAME", None)
		PROJECT_ID = os.environ.get("GCP_PROJECT_ID", None)
		INSTANCE_NAME = os.environ.get("GCP_INSTANCE_NAME", None)
		SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
		SQLALCHEMY_TRACK_MODIFICATIONS = True

	# Site Informations
	SITE_NAME = "TRADRDV"
	SITE_DESCRIPTION = _l("Traducteurs sur Rendez-vous est la première plateforme qui regroupe des traducteurs freelancers algériens, "\
		 "et bientôt des prestataires des quatre coins du monde !")
	SITE_ICONE = "https://storage.googleapis.com/tradrdv/dev/favicon.png"
	MAIL_CONTACT = 'contact@tradrdv.com'
	CALL_CONTACT = '+213 658489196'
	FAX_CONTACT = '---'
	ADDRESS = '42000, Tipasa, Algérie'

	ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", None) 
	ADMIN_FULLNAME = os.environ.get("ADMIN_FULLNAME", None) 
	ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", None)
	ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", None)
	TESTEUR_USERNAME = os.environ.get("TESTEUR_USERNAME", None) 
	TESTEUR_FULLNAME = os.environ.get("TESTEUR_FULLNAME", None) 
	TESTEUR_EMAIL = os.environ.get("TESTEUR_EMAIL", None)
	TESTEUR_PASSWORD = os.environ.get("TESTEUR_PASSWORD", None)

	COUNTRIES = ['Maroc', 'Tunisie', 'Algérie']
	TOWNS = {'Maroc':['Casablanca', 'Fés', 'Marrakech'], 'Tunisie':['Tunis', 'Sfax', 'Sousse '], 'Algérie':['Alger', 'Blida']}
	SKILLS = ['Français-Anglais', 'Français-Arabe', 'Français-Ruisse', 'Français-Italien', 'Français-Espagnol', 'Français-Chinois',\
		 'Arabe-Anglais', 'Arabe-Ruisse', 'Arabe-Italien', 'Arabe-Espagnol', 'Arabe-Chinois', 'Ruisse-Italien', 'Ruisse-Espagnol',\
			'Ruisse-Chinois', 'Italien-Espagnol', 'Italien-Chinois', 'Espagnol-Chinois']
	ePAYMENT_TYPES = ['PayPal', 'Payonner', 'Western Union', 'Compte Bancaire']
	STATUTS = ['admin', 'testeur', 'traducteur', 'client']
	SEX = ['Féminin', 'Masculin']
	PAYMENT_WAY = ['Payer cash', 'Abonnement']
	TRADUCTEUR_CAUTION = {'price_eur': 80.00, 'price_da': 15000}
	OFFRE_STATUTS = {'gratuit':{'price_eur': 0.0, 'price_da': 0}, 'standard':{'price_eur': 55.00, 'price_da': 7500}, 'premium':{'price_eur': 80.00, 'price_da': 11000}}
	COVER_PICTURE = 'https://storage.googleapis.com/tradrdv/dev/OOjs_UI_icon_userAvatar.svg.png'
	ORDER_PER_PAGE = 3

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
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
	ADMINS = ['contact@tradrdv.com', 'admin@tradrdv.com', 'programm01dev@gmail.com']
	# flask babel translator
	LANGUAGES = ['fr', 'en']
 