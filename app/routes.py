from flask import render_template, make_response, url_for, redirect, flash, request, jsonify, g
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from PIL import Image
import requests, json, os 
from datetime import datetime, timedelta
from flask_babel import _, get_locale
from googletrans import Translator


from app import app, db, client
from app.models import Chat, Deal, User, Traducteur, Contact, Newsletter
from app.utils import get_google_provider_cfg, allowed_image, delete_blob_img, upload_blob_img, upload_blob_file, password_reset_email,\
     email_confirm_email, alert_email, newsletter_email, sendgrid_mail
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchUserToLivreurForm, SearchGestionProduitForm, SearchOrderByEmailForm,\
    ContactForm
from app.decorators import check_confirmed, check_admin, check_manager, in_development


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

# @app.context_processor
# def my_utility_processor(): 
#     def translate(text=''): 
#         ts=Translator()
#         if not g.locale is 'fr':
#             try:
#                 output=text #output = ts.translate(text, src='auto', dest=g.locale).text
#             except Exception as e:
#                 output = text
#             except:
#                 output = text
#             return output
#         else:
#             return text    
#     return dict(translate=translate)




# -------------------------------------------------#
#--------------Home treatement program-------------#
#--------------------------------------------------#
@app.route('/')
@app.route('/accueil')
def accueil():
    #sendgrid_mail()
    return render_template('accueil.html', title=_('Accueil - ')+app.config['SITE_NAME'])



# -------------------------------------------------#
#--------------user treatement program-------------#
#--------------------------------------------------#
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('accueil', _external=True))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, fullname=form.fullname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Félicitations, vous êtes maintenant un utilisateur enregistré !'), 'success')
        return redirect(url_for('login', _external=True))
    return render_template('register.html', form=form, title=_('Inscription- ')+app.config['SITE_NAME'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accueil', _external=True))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('E-mail ou mot de passe invalide'), 'danger')
            return redirect(url_for('login', _external=True))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('accueil', _external=True)
        return redirect(next_page)
    return render_template('login.html', title=_('Connexion- ')+app.config['SITE_NAME'], form=form)  


@app.route("/login/google/")
def google_login():
    if current_user.is_authenticated:
        logout_user()
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg(app.config['GOOGLE_DISCOVERY_URL'])
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "callback",
        scope=["openid", "email", "profile"],)
    return redirect(request_uri)


@app.route("/login/google/callback")
def google_callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg(app.config['GOOGLE_DISCOVERY_URL'])
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code)
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']))
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        avatar = userinfo_response.json()["picture"]
        user_name = userinfo_response.json()["given_name"]
    else:
        flash(_('Une erreur s\'est produite, veuillez réessayer avec un autre compte gmail'), 'danger')
        return redirect(url_for('accueil', _external=True))
    # Doesn't exist? Add it to the database.
    user = User.query.filter_by(email=user_email).first()
    if user is None:
        user = User(fullname=user_name, email=user_email, google_login=True, confirmed=True)
        user.set_password(app.config['SOCIAL_LOGIN_PWD'])
        db.session.add(user)
        db.session.commit()
        login_user(User.query.filter_by(email=user_email).first(), remember=True)
        flash(_('Inscription avec votre compte google réussie'), 'success')
        # Send user back to homepage
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('accueil', _external=True)
        return redirect(next_page)
    login_user(User.query.filter_by(email=user_email).first(), remember=True)
    flash(_('Connexion avec votre compte google réussie'), 'success')
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('accueil', _external=True)
    return redirect(next_page)


@app.route('/update_profile/', methods=['POST', 'GET'])
@login_required
@check_confirmed
def update_profile():
    username = request.form.get('username')
    country = request.form.get('country')
    pseudo_com = request.form.get('pseudo_com')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    size = request.form.get('size')
    sex = request.form.get('sex')
    avatar_url = current_user.avatar

    uploaded_file = request.files.get("image")
    if uploaded_file:
        if int(size) <= app.config["MAX_IMAGE_FILESIZE"]:      
            if allowed_image(uploaded_file.filename):
                uploaded_file.filename = secure_filename(str(datetime.timestamp(datetime.now()))+uploaded_file.filename)
                Image.open(uploaded_file).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'cloud_img', uploaded_file.filename))
                delete_blob_img(app.config['CLOUD_STORAGE_BUCKET'], avatar_url)
                avatar_url = upload_blob_img(app.config['CLOUD_STORAGE_BUCKET'], uploaded_file, 'profile_img')
            else:
                flash(_('Erreur de nom ou d\'extension de l\'image'), 'danger')
                return redirect(url_for('track_order', id=current_user.id, _external=True))
        else:
            flash(_('Veuillez choisir une image de taille inférieur à 3Mo.'), 'danger')
            return redirect(url_for('track_order', id=current_user.id, _external=True))
    user = User.query.filter_by(email=current_user.email).first()
    if user.google_login is False:
        if old_password != '' and new_password != '':
            if user is None or not user.check_password(old_password):
                flash(_('Ancien mot de passe incorrect'), 'danger')
                return redirect(url_for('profile', _external=True))
            user.set_password(new_password)

    if username == '':
        flash(_('Veuillez fournir un nom d\'utilisateur'), 'danger')
        return redirect(url_for('profile', _external=True))
    elif User.query.filter_by(username=username).first():
        if username != user.username:
            flash(_('Veuillez fournir un nom d\'utilisateur correct'), 'danger')
            return redirect(url_for('profile', _external=True))

    if pseudo_com !='':
        parrain = User.query.filter((User.username==pseudo_com) & (User.ad_statut==True)).first()
        if parrain:
            if username == user.username:
                flash(_('Pseudo du parrain fournit est incorrect'), 'danger')
                return redirect(url_for('profile', _external=True))
        else:
            flash(_('Pseudo du parrain fournit est incorrect'), 'danger')
            return redirect(url_for('profile', _external=True))

    user.username = username if username != '' else current_user.username
    user.country = country if country != '' else current_user.country
    user.pseudo_com = pseudo_com if pseudo_com != '' else current_user.pseudo_com
    user.sex = sex if sex != '' else current_user.sex
    user.avatar = avatar_url
    db.session.commit()
    flash(_('Votre profil a bien été modifié'), 'success')
    return redirect(url_for('profile', _external=True))


@app.route('/confirm_email/')
@login_required
def confirm_email():
    if current_user.confirmed:
        return redirect(url_for('accueil', _external=True))
    email_confirm_email(current_user)
    flash(_('Vérifiez votre e-mail (ou spam) pour obtenir les instructions pour confirmer votre adresse mail'), 'warning')
    return redirect(url_for('accueil', _external=True))


@app.route('/confirmed_email/<token>', methods=['GET', 'POST'])
def confirmed_email(token):
    user = User.verify_confirm_email_token(token)
    if not user:
        flash(_('Le lien est expiré, veuillez réessayer !'), 'danger')
        return redirect(url_for('accueil', _external=True))
    user.set_confirmed(True)
    db.session.commit()
    flash(_('Votre adresse mail a bien été vérifié'))
    return redirect(url_for('profile', _external=True))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('accueil', _external=True))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            password_reset_email(user)
        flash(_('Vérifiez votre e-mail (ou spam) pour obtenir les instructions pour réinitialiser votre mot de passe'), 'success')
        return redirect(url_for('accueil', _external=True))
    return render_template('forgot_password.html', title=_('Réinitialiser votre mot de passe'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('accueil', _external=True))
    user = User.verify_reset_password_token(token)
    if not user:
        flash(_('Le lien est expiré, veuillez réessayer !'), 'danger')
        return redirect(url_for('forgot_password', _external=True))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Votre mot de passe a bien été réinitialisé, connectez-vous !'), 'success')
        return redirect(url_for('login', _external=True))
    return render_template('reset_password.html', form=form, title=_('Réinitialiser votre mot de passe'))


@app.route('/profile/')
@login_required 
@check_confirmed
def profile():
    if current_user.username is None:
        flash(_('Veuillez complèter votre profil et profiter pleinement de %(sitename)s', sitename=app.config['SITE_NAME']), 'warning')
    subtitle = _("Anonyme") if current_user.username is None else current_user.username
    deals = Deal.query.filter_by(user_id=current_user.id).order_by(Deal.timestamp.desc()).all()
    return render_template('profile.html', deals=deals, title=_("Profil- %(subtitle)s", subtitle=subtitle))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accueil', _external=True))



# -------------------------------------------------#
#-------Traducteur et Testeur panel   -------------#
#--------------------------------------------------#
@app.route('/traducteur/new')
@login_required
@check_confirmed
def traducteur_new():
    if current_user.statut == "traducteur" or current_user.statut == "testeur" or current_user.statut == "admin":
        flash(_('Vous êtes déjà souscrire à cette offre ou vous n\'êtes pas autorisé'), 'warning')
        return redirect(url_for('profile', _external=True))
    testeurs = User.query.filter((User.statut=='testeur') & (Traducteur.dispo==True) & (Traducteur.compte_valid==True))\
        .order_by(User.last_seen.asc()).all()
    return render_template('new_traducteur.html', testeurs=testeurs, title=_('Devenir traducteur'))


@app.route('/traducteur/new/register', methods=['GET', 'POST'])
@login_required
@check_confirmed
def traducteur_new_register():
    if current_user.statut == "traducteur" or current_user.statut == "testeur" or current_user.statut == "admin":
        flash(_('Vous êtes déjà souscrire à cette offre ou vous n\'êtes autorisé'), 'warning')
        return redirect(url_for('profile', _external=True))

    skill_1 = request.form.get('skill_1')
    skill_2 = request.form.get('skill_2')
    skill_3 = request.form.get('skill_3')
    skill_4 = request.form.get('skill_4')
    skill_5 = request.form.get('skill_5')
    skill_6 = request.form.get('skill_6')
    skill_7 = request.form.get('skill_7')
    skill_8 = request.form.get('skill_8')
    skill_9 = request.form.get('skill_9')
    skill_10 = request.form.get('skill_10')

    testeur_id = request.form.get('testeur_id')
    country = request.form.get('country')
    town = request.form.get('town')
    addr_postale = request.form.get('addr_postale')
    phone = request.form.get('phone')
    CCP_number = request.form.get('CCP_number')
    BaridiMob_RIP = request.form.get('BaridiMob_RIP')
    ePayment_type = request.form.get('ePayment_type')
    ePayment = request.form.get('ePayment')
    about_me = request.form.get('about_me')
    traducteur = True if request.form.get('traducteur') == 'on' else False
    interprete = True if request.form.get('interprete') == 'on' else False

    id_card = request.files.get("id_card")
    diploma = request.files.get("diploma")

    if id_card:
        if allowed_image(id_card.filename):
            id_card.filename = secure_filename(str(datetime.timestamp(datetime.now()))+id_card.filename)
            Image.open(id_card).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'cloud_img', id_card.filename))
            id_card = upload_blob_img(app.config['CLOUD_STORAGE_BUCKET'], id_card, 'id_card_img')
        else:
            flash(_('Erreur de nom ou d\'extension du carte identité/passeport'), 'danger')
            return redirect(url_for('traducteur_new_post', _external=True))
    else:
        id_card = 'https://storage.googleapis.com/tradrdv/dev/88591.png'

    if diploma:
        diploma.filename = secure_filename(str(datetime.timestamp(datetime.now()))+diploma.filename)
        diploma.save(os.path.join('app', 'static', 'assets', 'images', 'cloud_file', diploma.filename))
        diploma = upload_blob_file(app.config['CLOUD_STORAGE_BUCKET'], diploma, 'diploma_file')
    else:
        diploma = 'https://storage.googleapis.com/tradrdv/dev/diploma.pdf'

    traducteur = Traducteur(skill_1=skill_1, skill_2=skill_2, skill_3=skill_3, skill_4=skill_4, skill_5=skill_5, skill_6=skill_6, skill_7=skill_7,\
        skill_8=skill_8, skill_9=skill_9, skill_10=skill_10, current_country=country, current_town=town, addr_postale=addr_postale, phone=phone,\
        CCP_number=CCP_number, BaridiMob_RIP=BaridiMob_RIP, ePayment_type=ePayment_type, ePayment=ePayment, about_me=about_me,\
        traducteur=traducteur, interprete=interprete, author=current_user)
    db.session.add(traducteur)

    # Setup a deal (type of deal= service, work)
    testeur = User.query.filter_by(id=testeur_id).first()
    motif = 'Paiement de caution annuelle de traducteur'
    deal = Deal(type_deal='service', payment_way='Payer cash', motif=motif, amount=app.config['TRADUCTEUR_CAUTION']['price_da'],\
        friend=testeur, author=current_user)
    user = User.query.filter_by(id=current_user.id).first()
    user.statut = 'traducteur'
    db.session.add(deal)
    db.session.commit()

    chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==testeur.id)) | ((Chat.user_id==testeur.id) & (Chat.receiver_id==current_user.id))).first()
    if chat:
        chat.last_chat = datetime.utcnow()
    else:
        chat = Chat(receiver_id=testeur.id, author=current_user)
    message = "Bonjour,"
    contact = Contact(receiver_id=testeur.id, message=message, file_statut=False, author=current_user)
    db.session.add(contact)
    db.session.commit()
    if testeur.last_seen + timedelta(minutes=10) < datetime.utcnow():
        subject = _('Un nouveau message')
        body = _("Depuis votre dernière visite sur TRADRDV, %(username)s un nouveau traducteur aimerait passer son test d\'attitude auprès de vous."\
            "Veuillez consulter votre messagerie.", username=current_user.fullname) 
        url = url_for('profile', _external=True)
        alert_email(subject, body, url, testeur)
    flash(_('Veuillez payer la facture, joindre la photo du reçu et ensuite passez le test auprès du testeur'), 'success')
    return redirect(url_for('profile', _external=True))


@app.route('/manager/panel')
@login_required
@check_confirmed
@check_manager
@in_development
def manager_panel():
    if current_user.username is None:
        flash(_('Veuillez complèter et profiter pleinement de %(sitename)s', app.config['SITE_NAME']), 'warning')
    subtitle = _("Anonyme") if current_user.username is None else current_user.username
    # Get the deals in progress and finished for traducteur
    deals_progress = Deal.query.filter((Deal.friend_id==current_user.id) & (Deal.deal_over==False)).order_by(Deal.timestamp.desc()).all()
    deals_over = Deal.query.filter_by((Deal.friend_id==current_user.id) & (Deal.deal_over==True)).order_by(Deal.timestamp.desc()).all()

    return render_template('manager_panel.html', deals_progress=deals_progress, deals_over=deals_over, title=_("Profil- %(subtitle)s", subtitle=subtitle))


@app.route('/traducteur')
@in_development
def traducteur():
    return render_template('traducteur.html', title=_('Traducteur- ')+app.config['SITE_NAME'])

@app.route('/get/town/<country>', methods=['GET', 'POST'])
def get_town(country):
    towns = app.config["TOWNS"][country]
    return jsonify({'towns': towns}), 200


@app.route('/get/testeur/<testeur_id>', methods=['GET', 'POST'])
def get_testeur(testeur_id):
    testeur = Traducteur.query.filter_by(user_id=testeur_id).first()
    return jsonify({'testeur': testeur.as_dict()}), 200




# -------------------------------------------------#
#-------Messagerie route treatement program--------#
#--------------------------------------------------#
@app.route('/contact_us', methods=['POST', 'GET'])
@login_required
@check_confirmed
def contact_us():
    admin = User.query.filter((User.statut=='admin') & (User.id!=current_user.id)).order_by(User.last_seen.desc()).first()
    if admin:
        chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==admin.id)) |\
            ((Chat.user_id==admin.id) & (Chat.receiver_id==current_user.id))).first()
        if chat:
            chat.last_chat = datetime.utcnow()
        else:
            chat = Chat(receiver_id=admin.id, author=current_user)
        message = "Bonjour,"
        contact = Contact(receiver_id=admin.id, message=message, file_statut=False, author=current_user)
        db.session.add(contact)
        db.session.commit()
        if admin.last_seen + timedelta(minutes=10) < datetime.utcnow():
            subject = _('Un nouveau message')
            body = _('Depuis votre dernière visite sur TRADRDV, %(username)s aimerait entrer en contact avec vous.\
                Veuillez consulter votre messagerie.', username=current_user.fullname) 
            url = url_for('profile', _external=True)
            alert_email(subject, body, url, admin)
        return redirect(url_for('profile', _external=True))
    flash(_('Vous n\'être pas autorisés à effectuer cette opération'), 'warning')
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('profile', _external=True)
    return redirect(next_page)

@app.route('/post/message', methods=['GET', 'POST'])
@login_required
@check_confirmed
def send_message():
    msg_file = request.files.get('msg_file')
    msg_text = request.form.get('msg_text')
    receiver_id = request.form.get('receiver_id')
    file_statut = True if request.form.get('file_statut') == 'true' else False
   
    user = User.query.filter_by(id=receiver_id).first()
    if user:
        chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==user.id)) |\
             ((Chat.user_id==user.id) & (Chat.receiver_id==current_user.id))).first()
        if chat:
            chat.last_chat = datetime.utcnow()
        else:
            chat = Chat(receiver_id=user.id, author=current_user)
        if file_statut:
            msg_file.filename = secure_filename(str(datetime.timestamp(datetime.now()))+msg_file.filename)
            msg_file.save(os.path.join('app', 'static', 'assets', 'images', 'cloud_file', msg_file.filename))
            msg_file = upload_blob_file(app.config['CLOUD_STORAGE_BUCKET'], msg_file, 'message_file')
            
            contact = Contact(receiver_id=receiver_id, file=msg_file, file_statut=file_statut, author=current_user)
            db.session.add(contact)
            db.session.commit()
        else:
            contact = Contact(receiver_id=receiver_id, message=msg_text, author=current_user)
            db.session.add(contact)
            db.session.commit()
        if user.last_seen + timedelta(minutes=10) < datetime.utcnow():
            subject = _('Un nouveau message')
            body = _('Depuis votre dernière visite sur TRADRDV, %(username)s vous a envoyé un message.\
                Veuillez consulter votre messagerie.', username=current_user.fullname) 
            url = url_for('profile', _external=True)
            alert_email(subject, body, url, user)      
    return jsonify({}), 200


@app.route('/get/message', methods=['GET', 'POST'])
@login_required
@check_confirmed
def get_message():
    receiver_id = request.form.get('receiver_id')
    chats = Chat.query.filter((Chat.user_id==current_user.id) | (Chat.receiver_id==current_user.id)).all()
    user = User.query.filter_by(id=current_user.id).first()
    chats = [chat.as_dict() for chat in chats]
    if receiver_id == "":
        return jsonify({'messages': [], 'chats': chats, 'user': user.as_dict()}), 200
    messages = Contact.query.filter(((Contact.user_id==current_user.id) & (Contact.receiver_id==receiver_id)) |\
         ((Contact.user_id==receiver_id) & (Contact.receiver_id==current_user.id))).order_by(Contact.timestamp.asc()).all()
    messages = [message.as_dict() for message in messages]
    return jsonify({'messages': messages, 'chats': chats, 'user': user.as_dict()}), 200


@app.route('/newsletter/add', methods=['GET', 'POST'])
def newsletter_add():
    email=request.form.get('subscribe')
    follower = Newsletter.query.filter_by(email=email).first()
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('accueil', _external=True)
    if follower:
        flash(_('Cette adresse mail a déjà été enregistrée'), 'danger')
        return redirect(next_page)
    follower = Newsletter(email=email)
    db.session.add(follower)
    db.session.commit()
    flash(_('Merci pour la souscription'), 'success')
    return redirect(next_page)


@app.route('/send/message', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def send_messagel():
    msg_sending=True if request.form.get('msg_sending') == 'true' else False
    id=request.form.get('id')
    subject=request.form.get('subject')
    message=request.form.get('message')

    if msg_sending:
        contact = Contact.query.filter_by(id=id).first_or_404()
        emails = [contact.email]
        subject = '[Réponse] '+contact.subject
        body = message
        url = url_for('accueil', _external=True)
        newsletter_email(emails, subject, body, url, contact.username)

        contact.response = message
        contact.read = True
        db.session.commit()
        flash(_('Réponse envoyée'), 'success')
    else:
        emails = []  
        followers = Newsletter.query
        if followers.count() > 0:
            emails = [follower.email for follower in followers.all()]
            url = url_for('accueil', _external=True)
            newsletter_email(emails, subject, message, url)
            flash(_('Le broadcast est envoyé'), 'success')
            return redirect(url_for('messagerie', _external=True))
        flash(_('Vour n\'avez aucun contact pour le moment'), 'danger')
    return redirect(url_for('messagerie', _external=True))


@app.route('/messagerie')
@login_required
@check_confirmed
@check_admin
def messagerie():
    page = request.args.get('page', 1, type=int)

    messages = Contact.query.filter_by(read=False).paginate(page, app.config['ORDER_PER_PAGE'], False)
    next_url = url_for('messagerie', page=messages.next_num, _external=True) if messages.has_next else None
    prev_url = url_for('messagerie', page=messages.prev_num, _external=True) if messages.has_prev else None
    
    newsletter_subscribe = Newsletter.query.count()
    return render_template('messagerie.html', messages=messages.items, next_url=next_url, prev_url=prev_url, has_next=messages.has_next,\
        has_prev=messages.has_prev, newsletter_subscribe=newsletter_subscribe, page=page, title=_('Gestion messagerie et journal'))



# -------------------------------------------------#
#-------Admin route treatement program-------------#
#--------------------------------------------------#
@app.route('/admin/panel')
@login_required
@check_confirmed
@check_admin
@in_development
def admin_panel():
    if current_user.username is None:
        flash(_('Veuillez complèter et profiter pleinement de %(sitename)s', app.config['SITE_NAME']), 'warning')
    subtitle = _("Anonyme") if current_user.username is None else current_user.username
    return render_template('admin_panel.html', title=_("Profil- %(subtitle)s", subtitle=subtitle))






# -------------------------------------------------#
#-------Other route treatement program-------------#
#--------------------------------------------------#
@app.route('/get/notification', methods=['GET', 'POST'])
@login_required
@check_confirmed
def get_notification():
    number_new_msg = Contact.query.filter_by(read=False).count()
    return jsonify({'number_new_msg':number_new_msg}), 200


@app.route('/about_us')
def about_us():
    return render_template('about.html', title=_('À Propos de nous'))


@app.route('/news')
@in_development
def news():
    return render_template('news.html', title=_('Articles-')+app.config['SITE_NAME'])


@app.route('/terms')
@in_development
def terms():
    return render_template('terms.html', title=_('Conditions d\'utilisation'))


@app.route('/privacy')
@in_development
def privacy():
    return render_template('privacy.html', title=_('Politique de Confidentialité'))



# -------------------------------------------------#
#------errorhandler route treatement program-------#
#--------------------------------------------------#
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title=_("404 Erreur")), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title=_("500 Erreur")), 500