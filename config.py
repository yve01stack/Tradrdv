from flask_babel import lazy_gettext as _l
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY', None)
	SCHEDULER_API_ENABLED = True
	# Database initialization
	if os.environ.get('DATABASE_URL') is None:
		basedir = os.path.abspath(os.path.dirname(__file__))
		SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
		SQLALCHEMY_TRACK_MODIFICATIONS = False
	else:
		#PASSWORD = os.environ.get("GCP_INSTANCE_PWD", None)
		#PUBLIC_IP_ADDRESS = os.environ.get("GCP_PUBLIC_IP_ADDRESS", None)
		#DBNAME = os.environ.get("GCP_DB_NAME", None)
		#PROJECT_ID = os.environ.get("GCP_PROJECT_ID", None)
		#INSTANCE_NAME = os.environ.get("GCP_INSTANCE_NAME", None)
		#SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
		SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
		SQLALCHEMY_TRACK_MODIFICATIONS = True

	# Site Informations
	SITE_NAME = "TRADRDV"
	SITE_DESCRIPTION = _l("Traducteurs sur Rendez-vous est la première plateforme qui regroupe des traducteurs freelancers algériens, "\
		 "et bientôt des prestataires des quatre coins du monde !")
	SITE_ICONE = os.path.join('assets', 'images', 'dev', 'favicon.png').replace("\\", '/')
	MAIL_CONTACT = 'traducteurs.contactofficiel@gmail.com'
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

	COUNTRIES = ['Afghanistan (pashtou-dari)', 'Afrique du Sud (anglais)', 'Albanie (albanais)', 'Algérie (arabe)', 'Allemagne (allemand)', 'Andorre (catalan)',
		'Angola (portugais)', 'Antigua-et-Barbuda (anglais)', 'Arabie Saoudite (arabe)', 'Argentine (espagnol)', 'Arménie (arménien)', 'Australie (anglais)',
		'Autriche (allemand)', 'Azerbaïdjan (azéri)', 'Bahamas (anglais)', 'Bahreïn (arabe)', 'Bangladesh (bengali)', 'Barbade (anglais)', 'Belau / Palau / Palaos (anglais-paloasien)',
		'Belgique (néerlandais-français-allemand)', 'Belize (anglais)', 'Bénin (français)', 'Bhoutan (dzonkha)', 'Biélorussie (biélorusse-russe)',
		'Birmanie (birman)', 'Bolivie (espagnol)', 'Bosnie-Herzégovine (bosniaque-serbe-croate)', 'Botswana (anglais)', 'Brésil (portugais)', 'Brunei (malais)',
		'Bulgarie (bulgare)', 'Burkina Faso (français)', 'Burundi (kurindi-français)', 'Cambodge (khmer)', 'Cameroun (français-anglais)', 'Canada (anglais-français)',
		'Cap-Vert (portugais-créole)', 'Centrafrique (sango-français)', 'Chili (espagnol)', 'Chine (chinois)', 'Chypre (grec-turc)', 'Colombie (espagnol)', 'Comores (français-arabe)',
		'Congo-Brazzaville (français)', 'Congo-Kinshasa ou RDC (français)', 'Corée du Nord (coréen)', 'Corée du Sud (coréen)', 'Costa Rica (espagnol)',
		'Côte d’Ivoire (français)', 'Croatie (croate)', 'Cuba (espagnol)', 'Danemark (danois)', 'Djibouti (français-arabe)', 'Dominique (anglais)',
		'Égypte (arabe)', 'Émirats arabes unis (arabe)', 'Équateur (espagnol)', 'Érythrée (tigrina)', 'Espagne (espagnol)', 'Estonie (estonien)', 'États-Unis (anglais)',
		'Éthiopie (amharique)', 'Fidji (îles) (anglais)', 'Finlande (finnois-suédois)', 'France (français)', 'Gabon (français)', 'Gambie (anglais)',
		'Géorgie (géorgien)', 'Ghana (anglais)', 'Grèce (grec)', 'Grenade (anglais)', 'Guatemala (espagnol)', 'Guinée-Bissau (portugais)', 'Guinée-Conakry (français)',
		'Guinée équatoriale (espagnol)', 'Guyana (anglais)', 'Haïti (français-créole)', 'Honduras (espagnol)', 'Hongrie (hongrois)', 'Inde (hindi-anglais)',
		'Indonésie (bahasa indonesia)', 'Irak (arabe)', 'Iran (farsi)', 'Irlande (irlandais-anglais)', 'Islande (islandais)', 'Italie (italien)', 'Jamaïque (anglais)',
		'Japon (japonais)', 'Jordanie (arabe)', 'Kazakhstan (kazakh)', 'Kenya (anglais-swahili)', 'Kirghizistan (kirghiz-russe)', 'Kiribati (anglais)',
		'Kosovo (albanais-serbe)', 'Koweït (arabe)', 'Laos (lao)', 'Lesotho (anglais-sotho)', 'Lettonie (letton)', 'Liban (arabe)', 'Liberia (anglais)',
		'Libye (arabe)', 'Liechtenstein (allemand)', 'Lituanie (lituanien)', 'Luxembourg (français)', 'Macédoine (macédonien)', 'Madagascar (malgache-français-anglais)',
		'Malaisie (malais)', 'Malawi (anglais)', 'Maldives (maldivien)', 'Mali (français)', 'Malte (maltais-anglais)', 'Maroc (arabe)', 'Marshall (anglais-marshallais)',
		'Maurice (île) (anglais)', 'Mauritanie (arabe)', 'Mexique (espagnol)', 'Micronésie', 'Fédération des État de (anglais)', 'Moldavie (moldave/roumain)',
		'Monaco (français)', 'Mongolie (mongol)', 'Monténégro (monténégrin)', 'Mozambique (portugais)', 'Namibie (anglais)', 'Nauru (anglais-nauruan)',
		'Népal (népali)', 'Nicaragua (espagnol)', 'Niger (français)', 'Nigeria (anglais)', 'Norvège (bokmål-nynorsk)', 'Nouvelle-Zélande (anglais-maori)',
		'Oman (arabe)', 'Ouganda (anglais)', 'Ouzbékistan (ouzbek)', 'Pakistan (anglais-ourdou)', 'Palestine (arabe, hébreux)', 'Panama (espagnol)',
		'Papouasie-Nouvelle-Guinée (anglais)', 'Paraguay (espagnol)', 'Pays-Bas (néerlandais)', 'Pérou (espagnol)', 'Philippines (filipino)', 'Pologne (polonais)',
		'Portugal (portugais)', 'Qatar (arabe)', 'République dominicaine (espagnol)', 'République tchèque (thèque)', 'Roumanie (roumain)', 'Royaume-Uni (anglais)',
		'Russie (russe)', 'Rwanda (kinyarwanda-français-anglais)', 'Saint-Christophe-et-Niévès (anglais)', 'Sainte-Lucie (anglais)', 'Saint-Marin (italien)',
		'Saint-Vincent-et-les-Grenadines (anglais)', 'Salomon (îles) (anglais)', 'São-Tomé-et-Príncipe (portugais)', 'Salvador (espagnol)', 'Samoa occidentales (samoan-anglais)',
		'Sénégal (français)', 'Serbie (serbe)', 'Seychelles (français-anglais-créole)', 'Sierra Leone (anglais)', 'Singapour (malais-chinois-tamoul-anglais)',
		'Slovaquie (slovaque)', 'Slovénie (slovène)', 'Somalie (somali)', 'Soudan (arabe)', 'Soudan du Sud (anglais)', 'Sri Lanka (cinghalais-tamoul)',
		'Suède (suédois)', 'Suisse (allemand-français-italien-romanche)', 'Surinam (néerlandais)', 'Swaziland (anglais-swat)', 'Syrie (arabe)', 'Tadjikistan (tadjik)',
		'Tanzanie (anglais-swahili)', 'Tchad (arabe-français)', 'Timor oriental (portugais et tétum)', 'Thaïlande (thaï)', 'Togo (français)', 'Tonga (anglais-tonguien)',
		'Trinité-et-Tobago (anglais)', 'Tunisie (arabe)', 'Turkménistan (turkmène)', 'Turquie (turc)', 'Tuvalu (tuvaluan-anglais)', 'Ukraine (ukrainien)',
		'Uruguay (espagnol)', 'Vanuatu (anglais-français)', 'Vatican (italien)', 'Venezuela (espagnol)', 'Vietnam (vietnamien)', 'Yémen (arabe)', 'Zambie (anglais)',
		'Zimbabwe (anglais)']

	TOWNS = {'Maroc (arabe)':['Casablanca', 'Fés', 'Marrakech'], 'Tunisie (arabe)':['Tunis', 'Sfax', 'Sousse '], 
		'Algérie (arabe)':['Adrar', 'Chlef', 'Laghouat', 'Oum El Bouaghi', 'Batna', 'Béjaïa', 'Biskra', 'Béchar', 'Blida', 'Bouira', 'Tamanrasset', 'Tébessa',
			'Tlemcen', 'Tiaret', 'Tizi Ouzou', 'Alger', 'Djelfa', 'Jijel', 'Sétif', 'Saïda', 'Skikda', 'Sidi Bel Abbès', 'Annaba', 'Guelma', 'Constantine',
			'Médéa', 'Mostaganem', 'M\'Sila', 'Mascara', 'Ouargla', 'Oran', 'Bayadh', 'Illizi', 'Bordj Bou Arreridj', 'Boumerdès', 'El Tarf', 'Tindouf', 'Tissemsilt',
			'El Oued', 'Khenchela', 'Souk Ahras', 'Tipaza', 'Mila', 'Aïn Defla', 'Naâma', 'Aïn Témouchent', 'Ghardaïa', 'Relizane', 'Timimoun', 'Bordj Badji Mokhtar', 
			'Ouled Djellal', 'Béni Abbès', 'In Salah', 'In Guezzam', 'Touggourt', 'Djanet', 'El M\'Ghair', 'El Meniaa'],
		'Cameroun (français-anglais)':['Douala', 'Yaoundé', 'Garoua', 'Bamenda', 'Maroua', 'Nkongsamba', 'Bafoussam', 'Ngaoundéré', 'Bertoua', 'Loum', 'Kumba', 'Edéa',
			'Kumbo', 'Foumban', 'Mbouda', 'Dschang', 'Limbé', 'Ebolowa', 'Kousséri', 'Guider', 'Meiganga', 'Yagoua', 'Mbalmayo', 'Bafang', 'Tiko', 'Bafia', 'Wum', 
			'Kribi', 'Buea', 'Sangmélima', 'Foumbot', 'Bangangté', 'Batouri', 'Banyo', 'Nkambé', 'Bali', 'Mbanga', 'Mokolo', 'Melong', 'Manjo', 'Garoua-Boulaï', 'Mora', 
			'Kaélé', 'Tibati', 'Ndop', 'Akonolinga', 'Eséka', 'Mamfé', 'Obala', 'Muyuka', 'Nanga-Eboko', 'Abong-Mbang', 'Fundong',	'Nkoteng', 'Fontem', 'Mbandjock', 
			'Touboro', 'Ngaoundal', 'Yokadouma', 'Pitoa', 'Tombel', 'Kékem', 'Magba', 'Bélabo', 'Tonga', 'Maga', 'Koutaba', 'Blangoua', 'Guidiguis', 'Bogo', 'Batibo', 
			'Yabassi', 'Figuil', 'Makénéné', 'Gazawa', 'Tcholliré']}

	SKILLS=['Arabe-français', 'Arabe-tamazight', 'Arabe-espagnol', 'Arabe-portugais', 'Arabe-italien', 'Arabe-anglais', 'Arabe-allemand', 'Arabe-polonais',
		'Arabe-turc', 'Arabe-ukrainien', 'Arabe-russe', 'Arabe-Chinois', 'Tamazight–arabe', 'Tamazight-Français', 'Tamazight-espagnol', 'Tamazight-portugais',
		'Tamazight-italien', 'Tamazight-anglais', 'Tamazight-allemand', 'Tamazight-polonais', 'Tamazight-turc', 'Tamazight-ukrainien', 'Tamazight-russe', 'Tamazight-chinois',
		'Français–arabe', 'Français–tamazight', 'Français–espagnol', 'Français–portugais', 'Français–italien', 'Français–anglais', 'Français–allemand', 'Français–polonais',
		'Français–turc', 'Français–ukrainien', 'Français–russe', 'Français–chinois', 'Espagnol-arabe', 'Espagnol-tamazight', 'Espagnol-français', 'Espagnol-espagnol', 
		'Espagnol-portugais', 'Espagnol-italien', 'Espagnol-anglais', 'Espagnol-allemand', 'Espagnol-polonais', 'Espagnol-turc', 'Espagnol-ukrainien', 
		'Espagnol-russe', 'Espagnol-chinois', 'Portugais-arabe', 'Portugais-tamazight', 'Portugais-français', 
		'Portugais-espagnol', 'Portugais-italien', 'Portugais-anglais', 'Portugais-allemand', 'Portugais-polonais', 'Portugais-turc', 'Portugais-ukrainien',
		'Portugais-russe', 'Portugais-chinois', 'Italien–arabe', 'Italien–tamazight', 'Italien–français', 'Italien–espagnol', 'Italien–portugais', 'Italien–anglais',
		'Italien–allemand', 'Italien–polonais', 'Italien–turc', 'Italien–ukrainien', 'Italien–russe', 'Italien–chinois', 'Anglais–arabe', 'Anglais–tamazight', 'Anglais–français',
		'Anglais–espagnol', 'Anglais–portugais', 'Anglais–italien', 'Anglais–allemand', 'Anglais–polonais', 'Anglais–turc', 'Anglais–ukrainien', 'Anglais–russe',
		'Anglais–chinois', 'Allemand–arabe', 'Allemand–tamazight', 'Allemand–français', 'Allemand–espagnol', 'Allemand–portugais', 'Allemand–italien',
		'Allemand–anglais', 'Allemand–polonais', 'Allemand–turc', 'Allemand–ukrainien', 'Allemand–russe', 'Allemand–chinois', 'Polonais–arabe', 'Polonais–tamazight',
		'Polonais–français', 'Polonais–espagnol', 'Polonais–portugais', 'Polonais–italien', 'Polonais–anglais', 'Polonais–allemand', 'Polonais–turc','Polonais–ukrainien',
		'Polonais–russe', 'Polonais–chinois', 'Turc–arabe', 'Turc–tamazight', 'Turc–français', 'Turc–espagnol', 'Turc–portugais', 'Turc–italien', 'Turc–anglais',
		'Turc–allemand', 'Turc–polonais', 'Turc–ukrainien', 'Turc–russe', 'Turc–chinois', 'Ukrainien–arabe', 'Ukrainien–tamazight', 'Ukrainien–français',
		'Ukrainien–espagnol', 'Ukrainien–portugais', 'Ukrainien–italien', 'Ukrainien–anglais', 'Ukrainien–allemand', 'Ukrainien–polonais', 'Ukrainien–truc',
		'Ukrainien–russe', 'Ukrainien–chinois', 'Russe-arabe', 'Russe-tamazight', 'Russe-français', 'Russe-espagnol', 'Russe-portugais', 'Russe-italien',
		'Russe-anglais', 'Russe-allemand', 'Russe-polonais', 'Russe-turc', 'Russe-ukrainien', 'Russe-chinois', 'Chinois-arabe', 'Chinois-tamazight', 'Chinois-français',
		'Chinois-espagnol', 'Chinois-portugais', 'Chinois-italien', 'Chinois-anglais', 'Chinois-allemand', 'Chinois-polonais', 'Chinois-turc', 'Chinois-ukrainien', 'Chinois- russe']
 
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
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	
	SENDGRID_KEY = os.environ.get('SENDGRID_KEY')
	EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
	EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
	EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
	EMAIL_HOST = os.environ.get('EMAIL_HOST')
	EMAIL_PORT = int(os.environ.get('EMAIL_PORT') or 2525)
	EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') is not True
	SENDGRID_NEED = os.environ.get('SENDGRID_NEED')

	ADMINS = ['contact@tradrdv.com', 'admin@tradrdv.com', 'programm01dev@gmail.com']
	# flask babel translator
	LANGUAGES = ['fr', 'en', 'es']
