from flask import render_template, make_response, url_for, redirect, flash, request, jsonify, g
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from PIL import Image
import requests, json, os 
from datetime import datetime, timedelta
from flask_babel import _, get_locale
from googletrans import Translator


from app import app, db, client, tasks
from app.models import Chat, Deal, Payment, User, Traducteur, Contact, Newsletter, Dashbord, Pub, Marketing, make_payment, get_paid
from app.utils import get_google_provider_cfg, allowed_image, password_reset_email,\
     email_confirm_email, alert_email, newsletter_email, select_by_random, return_eq_da
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
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
    this_month = Dashbord.query.filter_by(id=1).first()
    this_month.update_dashbord(accueil_view=1)

    #Dashbord of the two months
    dashbord_this_month = Dashbord.query.filter_by(id=1).first()
    dashbord_last_month = Dashbord.query.filter_by(id=2).first()

    traducteurs_need_ad = Traducteur.query.filter((Traducteur.compte_valid==True) & (Traducteur.need_help_ad=='on')).order_by(select_by_random()).all()
    traducteurs = Traducteur.query.filter((Traducteur.compte_valid==True)).order_by(select_by_random()).all()
    pubs = Pub.query.filter_by(valid=True).order_by(select_by_random()).all()
    return render_template('accueil.html', traducteurs_need_ad=traducteurs_need_ad, traducteurs=traducteurs, pubs=pubs,
        dashbord_this_month=dashbord_this_month, dashbord_last_month=dashbord_last_month, title=_('Accueil - %(sitename)s', sitename=app.config['SITE_NAME']))


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
    return render_template('register.html', form=form, title=_('Inscription - %(sitename)s', sitename=app.config['SITE_NAME']))


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
            #form.remember_me.data
        login_user(user, remember=False)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('accueil', _external=True)
        return redirect(next_page)
    return render_template('login.html', title=_('Connexion - %(sitename)s', sitename=app.config['SITE_NAME']), form=form)  


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
        login_user(User.query.filter_by(email=user_email).first(), remember=False)
        flash(_('Inscription avec votre compte google réussie'), 'success')
        # Send user back to homepage
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('accueil', _external=True)
        return redirect(next_page)
    login_user(User.query.filter_by(email=user_email).first(), remember=False)
    flash(_('Connexion avec votre compte google réussie'), 'success')
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('accueil', _external=True)
    return redirect(next_page)


@app.route('/upgrade_profile/', methods=['POST', 'GET'])
@login_required
@check_confirmed
def upgrade_profile():
    username = request.form.get('username')
    country = request.form.get('country')
    size = request.form.get('size')
    sex = request.form.get('sex')
    avatar_url = current_user.avatar

    uploaded_file = request.files.get("image")
    if uploaded_file:
        if int(size) <= app.config["MAX_IMAGE_FILESIZE"]:      
            if allowed_image(uploaded_file.filename):
                uploaded_file.filename = secure_filename(str(datetime.timestamp(datetime.now()))+uploaded_file.filename)
                Image.open(uploaded_file).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'profile_img', uploaded_file.filename))
                avatar_url = os.path.join('assets', 'images', 'profile_img', uploaded_file.filename).replace("\\", '/')
            else:
                flash(_('Erreur de nom ou d\'extension de l\'image'), 'danger')
                return redirect(url_for('profile', id=current_user.id, _external=True))
        else:
            flash(_('Veuillez choisir une image de taille inférieur à 3Mo.'), 'danger')
            return redirect(url_for('profile', id=current_user.id, _external=True))
    
    user = User.query.filter_by(email=current_user.email).first()
    if User.query.filter_by(username=username).first():
        if user.username != username:
            flash(_('Veuillez fournir un nom d\'utilisateur correct'), 'danger')
            return redirect(url_for('profile', _external=True))
    if username != '':
        user.username = current_user.username if not current_user.username is None and current_user.username !=''  else username
    if country != '':
        user.country = current_user.country if not current_user.country is None and current_user.country !='' else country
    if sex != '':
        user.sex = current_user.sex if not current_user.sex is None and current_user.sex !='' else sex

    number_deal = Deal.query.filter((Deal.user_id==current_user.id) & (Deal.deal_over==True)).count()
    if number_deal<5:
        if user.sex=='Féminin':
            user.avatar = os.path.join('assets', 'images', 'dev', 'sex_f.jpg').replace("\\", '/')
        elif user.sex=='Masculin':
            user.avatar = os.path.join('assets', 'images', 'dev', 'sex_m.jpg').replace("\\", '/')
        else:
            user.avatar = avatar_url
    else:
        user.avatar = avatar_url
    db.session.commit()
    flash(_('Votre profil a bien été modifié'), 'success')
    return redirect(url_for('profile', _external=True))

@app.route('/update_pwd/', methods=['POST', 'GET'])
@login_required
@check_confirmed
def update_pwd():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    user = User.query.filter_by(email=current_user.email).first()
    if user.google_login is False:
        if user is None or not user.check_password(old_password):
            flash(_('Ancien mot de passe incorrect'), 'warning')
            return redirect(url_for('profile', _external=True))
        user.set_password(new_password)
        db.session.commit()
        flash(_('Votre mot de passe a bien été modifié'), 'success')
    else:
        flash(_('Vous ne pouvez pas changer votre mot de passe car vous utilisez google login'), 'warning')
    return redirect(url_for('profile', _external=True))


@app.route('/set_parrain/', methods=['POST', 'GET'])
@login_required
@check_confirmed
def set_parrain():
    pseudo_com = request.form.get('pseudo_com')
    link_com = request.form.get('link_com')

    user = User.query.filter_by(email=current_user.email).first()
    parrain = User.query.filter((User.username==pseudo_com) & (User.ad_statut==True)).first()
    if parrain:
        if pseudo_com == user.username:
            flash(_('Pseudo du parrain fournit est incorrect'), 'danger')
            return redirect(url_for('profile', _external=True))
        else:
            user.pseudo_com = current_user.pseudo_com if not current_user.pseudo_com is None and current_user.pseudo_com !=''  else pseudo_com
            user.link_com = current_user.link_com if not current_user.link_com is None and current_user.link_com !=''  else link_com
            flash(_('Parrain est ajouté'), 'success')
            return redirect(url_for('profile', _external=True))
    flash(_('Pseudo du parrain fournit est incorrect'), 'danger')
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


@app.route('/offer/<offer_type>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def offer_subscribe(offer_type):
    user = User.query.filter_by(id=current_user.id).first()
    subscribe_in_progress = Deal.query.filter((Deal.user_id==current_user.id) & (Deal.type_deal=='abon') & (Deal.deal_over==False)).first()
    if user.remain_day > 0:
        flash(_('Désolé, vous avez un offre en cours'), 'warning')
        return redirect(url_for('accueil', _external=True))
    if subscribe_in_progress:
        flash(_('Désolé, vous avez une demande d\'offre en cours'), 'warning')
        return redirect(url_for('accueil', _external=True))
    
    admin = User.query.filter((User.statut=='admin')).order_by(User.last_seen.desc()).first()
    if offer_type == 'standard':
        motif = _('Souscription à l\'offre standard')
        deal = Deal(type_deal='abon', payment_way='cash', motif=motif, amount=app.config['OFFRE_STATUTS']['standard']['price_da'],\
            devise=app.config['DEVISES'][0]['symbol'], friend_accept=True, friend=admin, author=current_user)
    elif offer_type == 'premium':
        motif = _('Souscription à l\'offre premium')
        deal = Deal(type_deal='abon', payment_way='cash', motif=motif, amount=app.config['OFFRE_STATUTS']['premium']['price_da'],\
             devise=app.config['DEVISES'][0]['symbol'], friend_accept=True, friend=admin, author=current_user)
    else:
        return render_template('404.html', title=_("404 Erreur")), 404
    
    db.session.add(deal)
    db.session.commit()
    flash(_('Veuillez payer la facture, joindre la photo du reçu et ensuite profitez de votre offre'), 'success')
    return redirect(url_for('accueil', _external=True))
   

@app.route('/profile/')
@login_required 
@check_confirmed
def profile():
    if current_user.username is None:
        flash(_('Veuillez complèter votre profil et profiter pleinement de %(sitename)s', sitename=app.config['SITE_NAME']), 'warning')
    subtitle = _("Anonyme") if current_user.username is None else current_user.username
    deals = Deal.query.filter_by(user_id=current_user.id).order_by(Deal.timestamp.desc()).all()
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.timestamp.desc()).all()
    pubAccount = Marketing.query.filter((Marketing.user_id==current_user.id)).first()
    pubs = Pub.query.filter((Pub.user_id==current_user.id)).all()
    return render_template('profile.html', deals=deals, payments=payments, pubAccount=pubAccount, pubs=pubs,
        title=_("Profil- %(subtitle)s", subtitle=subtitle))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accueil', _external=True))


# -------------------------------------------------#
#------------------   ADs panel   -----------------#
#--------------------------------------------------#
@app.route('/create/pub', methods=['GET', 'POST'])
@login_required
@check_confirmed
def create_pub():
    account = Marketing.query.filter((Marketing.user_id==current_user.id)).first()
    if not account:
        new_account = Marketing(author=current_user)
        db.session.add(new_account)
        db.session.commit()
    
    account = Marketing.query.filter((Marketing.user_id==current_user.id)).first()
    pubs = Pub.query.filter((Pub.user_id==current_user.id))
    if not account.compte_valid:
        flash(_('Erreur, vous n\'avez aucun abonnement de marketing en cours'), 'danger')
        return redirect(url_for('profile', _external=True))
    elif account.nbr_pub <= pubs.count():
        flash(_('Erreur, vous avez déjà atteint le nombre maximal d\'article de votre abonnement en cours'), 'danger')
        return redirect(url_for('profile', _external=True))

    title = request.form.get('title')
    category = request.form.get('category')
    detail_1 = request.form.get('detail_1')
    detail_2 = request.form.get('detail_2')
    detail_3 = request.form.get('detail_3')
    ref_link = request.form.get('ref_link')
    description = request.form.get('description')
    image_1 = request.files.get("image_1")
    image_2 = request.files.get("image_2")

    if image_1:
        if allowed_image(image_1.filename):
            image_1.filename = secure_filename(str(datetime.timestamp(datetime.now()))+image_1.filename)
            Image.open(image_1).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'pub_img', image_1.filename))
            image_1 = os.path.join('assets', 'images', 'pub_img', image_1.filename).replace("\\", '/')
        else:
            flash(_('Erreur de nom ou d\'extension de la première image'), 'danger')
            return redirect(url_for('profile', _external=True))
    else:
        image_1 = os.path.join('assets', 'images', 'dev', '916733.png').replace("\\", '/')

    if image_2:
        if allowed_image(image_2.filename):
            image_2.filename = secure_filename(str(datetime.timestamp(datetime.now()))+image_2.filename)
            Image.open(image_2).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'pub_img', image_2.filename))
            image_2 = os.path.join('assets', 'images', 'pub_img', image_2.filename).replace("\\", '/')
        else:
            flash(_('Erreur de nom ou d\'extension de la deuxième image'), 'danger')
            return redirect(url_for('profile', _external=True))
    else:
        image_2 = os.path.join('assets', 'images', 'dev', '916733.png').replace("\\", '/')

    new_pub = Pub(title=title, category=category, detail_1=detail_1, detail_2=detail_2, detail_3=detail_3, ref_link=ref_link,
        description=description, image_1=image_1, image_2=image_2, valid=True, author=current_user)
    db.session.add(new_pub)
    db.session.commit()
    flash(_('Votre article a été crée avec succès'), 'success')
    return redirect(url_for('profile', _external=True))


@app.route('/pub/account/subscribe', methods=['GET', 'POST'])
@login_required
@check_confirmed
def pub_subscribe():
    account = Marketing.query.filter((Marketing.user_id==current_user.id)).first()
    if not account:
        new_account = Marketing(author=current_user)
        db.session.add(new_account)
        db.session.commit()

    account = Marketing.query.filter((Marketing.user_id==current_user.id)).first_or_404()
    if account.compte_valid:
        flash(_('Erreur, vous avez un abonnement de marketing en cours'), 'danger')
        return redirect(url_for('profile', _external=True))
    else:
        subscribe_in_progress = Deal.query.filter((Deal.user_id==current_user.id) & (Deal.type_deal=='abon_pub') & (Deal.deal_over==False)).first()
        if subscribe_in_progress:
            flash(_('Désolé, vous avez une demande d\'offre en cours'), 'warning')
            return redirect(url_for('profile', _external=True))
    
        admin = User.query.filter((User.statut=='admin')).order_by(User.last_seen.desc()).first()
        motif = _('Souscription à l\'abonnement marketing')
        deal = Deal(type_deal='abon_pub', payment_way='cash', motif=motif, amount=1000,\
            devise=app.config['DEVISES'][0]['symbol'], friend_accept=True, friend=admin, author=current_user)
        db.session.add(deal)
        db.session.commit()
    flash(_('Veuillez payer la facture, joindre la photo du reçu et ensuite profitez de votre abonnement marketing'), 'success')
    return redirect(url_for('profile', _external=True))
      

@app.route('/pub/activate/<pub_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def pub_activate(pub_id):
    pub = Pub.query.filter((Pub.id==pub_id) & (Marketing.user_id==current_user.id)).first_or_404()
    account = Marketing.query.filter((Marketing.user_id==current_user.id)).first()
    
    pubs = Pub.query.filter((Pub.user_id==current_user.id) & (Pub.valid==True))
    if not account.compte_valid:
        flash(_('Erreur, vous n\'avez aucun abonnement de marketing en cours'), 'danger')
        return redirect(url_for('profile', _external=True))
    elif account.nbr_pub <= pubs.count():
        flash(_('Erreur, vous avez déjà atteint le nombre maximal d\'article de votre abonnement en cours'), 'danger')
        return redirect(url_for('profile', _external=True))
    else:
        pub.valid = True
        db.session.commit()
        flash(_('Votre article est maintenant en ligne'), 'success')
    return redirect(url_for('profile', _external=True))

@app.route('/pub/update', methods=['GET', 'POST'])
@login_required
@check_confirmed
def pub_update():
    pub_id = request.form.get('pub_id')
    title = request.form.get('title')
    category = request.form.get('category')
    detail_1 = request.form.get('detail_1')
    detail_2 = request.form.get('detail_2')
    detail_3 = request.form.get('detail_3')
    ref_link = request.form.get('ref_link')
    description = request.form.get('description')
    image_1 = request.files.get("image_1")
    image_2 = request.files.get("image_2")
    pub = Pub.query.filter((Pub.id==pub_id) & (Marketing.user_id==current_user.id)).first_or_404()

    if image_1:
        if allowed_image(image_1.filename):
            image_1.filename = secure_filename(str(datetime.timestamp(datetime.now()))+image_1.filename)
            Image.open(image_1).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'pub_img', image_1.filename))
            image_1 = os.path.join('assets', 'images', 'pub_img', image_1.filename).replace("\\", '/')
        else:
            flash(_('Erreur de nom ou d\'extension de la première image'), 'danger')
            return redirect(url_for('profile', _external=True))
    else:
        image_1 = pub.image_1

    if image_2:
        if allowed_image(image_2.filename):
            image_2.filename = secure_filename(str(datetime.timestamp(datetime.now()))+image_2.filename)
            Image.open(image_2).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'pub_img', image_2.filename))
            image_2 = os.path.join('assets', 'images', 'pub_img', image_2.filename).replace("\\", '/')
        else:
            flash(_('Erreur de nom ou d\'extension de la deuxième image'), 'danger')
            return redirect(url_for('profile', _external=True))
    else:
        image_2 = pub.image_2
    
    account = Marketing.query.filter((Marketing.user_id==current_user.id)).first()
    pubs = Pub.query.filter((Pub.user_id==current_user.id) & (Pub.valid==True))
    if not account.compte_valid:
        flash(_('Erreur, vous n\'avez aucun abonnement de marketing en cours'), 'danger')
        return redirect(url_for('profile', _external=True))
    elif pubs.count() < account.nbr_pub:
        pub.title = title
        pub.category = category
        pub.detail_1 = detail_1
        pub.detail_2 = detail_2
        pub.detail_3 = detail_3
        pub.ref_link = ref_link
        pub.description = description        
        pub.image_1 = image_1
        pub.image_2 = image_2
        pub.valid = True
        db.session.commit()
        flash(_('Votre article a été modifié et est maintenant en ligne'), 'success')
        return redirect(url_for('profile', _external=True))
    elif pubs.count() == account.nbr_pub:
        if pub.valid:
            pub.title = title
            pub.category = category
            pub.detail_1 = detail_1
            pub.detail_2 = detail_2
            pub.detail_3 = detail_3
            pub.ref_link = ref_link
            pub.description = description
            pub.image_1 = image_1
            pub.image_2 = image_2
            db.session.commit()
            flash(_('Votre article a été modifié et est maintenant en ligne'), 'success')
            return redirect(url_for('profile', _external=True))
    flash(_('Erreur, vous avez déjà atteint le nombre maximal d\'article de votre abonnement en cours'), 'danger')
    return redirect(url_for('profile', _external=True))

@app.route('/pub/delete/<pub_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def pub_delete(pub_id):
    pub = Pub.query.filter((Pub.id==pub_id) & (Marketing.user_id==current_user.id)).first_or_404()
    db.session.delete(pub) 
    db.session.commit()
    flash(_('Votre article est bien été supprimé'), 'success')
    return redirect(url_for('profile', _external=True))

@app.route('/pub/view/<pub_id>/<category>', methods=['GET', 'POST'])
def pub_view(pub_id, category):
    pub = Pub.query.filter((Pub.id==pub_id) & (Pub.valid==True)).first_or_404()
    pubs = Pub.query.filter((Pub.valid==True) & (Pub.category==category)).order_by(select_by_random()).all()
    pub.add_clic()
    return render_template('single_pub.html', pub=pub, pubs=pubs, title=pub.title)

@app.route('/get/pub', methods=['GET', 'POST'])
@login_required
@check_confirmed
def get_pub():
    pub_id = request.form.get('pub_id')
    pub = Pub.query.filter((Pub.id==pub_id)).first()
    return jsonify({'pub': pub.as_dict()}), 200



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
    testeurs = User.query.filter((User.statut=='testeur')).order_by(User.last_seen.asc()).all()
    print(testeurs)
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
    prestation = request.form.get('prestation')
    prestation_2 = request.form.get('prestation_2')
    prestation_3 = request.form.get('prestation_3')
    prestation_4 = request.form.get('prestation_4')
    prestation_5 = request.form.get('prestation_5')
    prestation_6 = request.form.get('prestation_6')
    prestation_7 = request.form.get('prestation_7')

    id_card = request.files.get("id_card")
    diploma = request.files.get("diploma")

    if id_card:
        if allowed_image(id_card.filename):
            id_card.filename = secure_filename(str(datetime.timestamp(datetime.now()))+id_card.filename)
            Image.open(id_card).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'id_card_img', id_card.filename))
            id_card = os.path.join('assets', 'images', 'id_card_img', id_card.filename).replace("\\", '/')
        else:
            flash(_('Erreur de nom ou d\'extension du carte identité/passeport'), 'danger')
            return redirect(url_for('traducteur_new_post', _external=True))
    else:
        id_card = os.path.join('assets', 'images', 'dev', '88591.png').replace("\\", '/')

    if diploma:
        diploma.filename = secure_filename(str(datetime.timestamp(datetime.now()))+diploma.filename)
        diploma.save(os.path.join('app', 'static', 'assets', 'images', 'diploma_file', diploma.filename))
        diploma = os.path.join('assets', 'images', 'diploma_file', diploma.filename).replace("\\", '/')
    else:
        diploma = os.path.join('assets', 'images', 'dev', 'diploma.pdf').replace("\\", '/')

    new_traducteur = Traducteur(skill_1=skill_1, skill_2=skill_2, skill_3=skill_3, skill_4=skill_4, skill_5=skill_5, skill_6=skill_6, skill_7=skill_7,\
        skill_8=skill_8, skill_9=skill_9, skill_10=skill_10, current_country=country, current_town=town, addr_postale=addr_postale, phone=phone,\
        CCP_number=CCP_number, BaridiMob_RIP=BaridiMob_RIP, ePayment_type=ePayment_type, ePayment=ePayment, about_me=about_me, id_card=id_card, diploma=diploma,\
        prestation=prestation, prestation_2=prestation_2, prestation_3=prestation_3, prestation_4=prestation_4, prestation_5=prestation_5,
        prestation_6=prestation_6, prestation_7=prestation_7, author=current_user)
    db.session.add(new_traducteur)

    # Setup a deal (type of deal= trad, test, abon)
    testeur = User.query.filter_by(id=testeur_id).first()
    motif = _('Paiement de caution annuelle de traducteur')
    deal = Deal(type_deal='test', payment_way='cash', motif=motif, amount=app.config['TRADUCTEUR_CAUTION']['price_da'],\
        devise=app.config['DEVISES'][0]['symbol'], friend=testeur, author=current_user)
    user = User.query.filter_by(id=current_user.id).first()
    user.statut = 'traducteur'
    db.session.add(deal)
    db.session.commit()

    chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==testeur.id)) | ((Chat.user_id==testeur.id) & (Chat.receiver_id==current_user.id))).first()
    if chat:
        chat.last_chat = datetime.utcnow()
    else:
        chat = Chat(receiver_id=testeur.id, author=current_user)
    message = _("Nouveau accord: ")+motif
    contact = Contact(receiver_id=testeur.id, message=message, file_statut=False, author=current_user)
    db.session.add(contact)
    db.session.commit()
    if testeur.last_seen + timedelta(minutes=20) < datetime.utcnow():
        subject = _('Un nouveau message')
        body = _("Depuis votre dernière visite sur TRADRDV, %(username)s un nouveau traducteur aimerait passer son test d\'attitude auprès de vous."\
            "Veuillez consulter votre messagerie.", username=current_user.username) 
        url = url_for('profile', _external=True)
        alert_email(subject, body, url, testeur)
    flash(_('Veuillez payer la facture, joindre la photo du reçu et ensuite passez le test auprès du testeur'), 'success')
    return redirect(url_for('profile', _external=True))


@app.route('/manager/traducteur/update/<deal_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_manager
def trad_test_update(deal_id):
    deal = Deal.query.filter((Deal.id==deal_id) & (Deal.friend_id==current_user.id)).first_or_404()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('manager_panel', _external=True))

    traducteur = Traducteur.query.filter_by(user_id=deal.user_id).first_or_404()
    testeurs = User.query.filter((User.statut=='testeur')).order_by(User.last_seen.asc()).all()
    return render_template('update_traducteur.html', traducteur=traducteur, testeurs=testeurs, deal=deal, title=_('Mise à du compte traducteur'))


@app.route('/traducteur/update', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_manager
def traducteur_update():
    if current_user.statut == "traducteur" or current_user.statut == "admin":
        flash(_('Vous êtes déjà souscrire à cette offre ou vous n\'êtes autorisés'), 'warning')
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

    deal_id = request.form.get('deal_id')
    rate = request.form.get('rate') if not request.form.get('rate') is None else 1
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
    prestation = request.form.get('prestation')
    prestation_2 = request.form.get('prestation_2')
    prestation_3 = request.form.get('prestation_3')
    prestation_4 = request.form.get('prestation_4')
    prestation_5 = request.form.get('prestation_5')
    prestation_6 = request.form.get('prestation_6')
    prestation_7 = request.form.get('prestation_7')

    id_card = request.files.get("id_card")
    diploma = request.files.get("diploma")

    deal = Deal.query.filter((Deal.id==deal_id) & (Deal.friend_id==current_user.id)).first_or_404()
    traducteur_old = Traducteur.query.filter_by(user_id=deal.user_id).first_or_404()

    if id_card:
        if allowed_image(id_card.filename):
            id_card.filename = secure_filename(str(datetime.timestamp(datetime.now()))+id_card.filename)
            Image.open(id_card).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'id_card_img', id_card.filename))
            id_card = os.path.join('assets', 'images', 'id_card_img', id_card.filename).replace("\\", '/')
        else:
            flash(_('Erreur de nom ou d\'extension du carte identité/passeport'), 'danger')
            return redirect(url_for('traducteur_new_post', _external=True))
    else:
        id_card = traducteur_old.id_card

    if diploma:
        diploma.filename = secure_filename(str(datetime.timestamp(datetime.now()))+diploma.filename)
        diploma.save(os.path.join('app', 'static', 'assets', 'images', 'diploma_file', diploma.filename))
        diploma = os.path.join('assets', 'images', 'diploma_file', diploma.filename).replace("\\", '/')
    else:
        diploma = traducteur_old.diploma

    traducteur_old.skill_1 = skill_1
    traducteur_old.skill_2 = skill_2
    traducteur_old.skill_3 = skill_3
    traducteur_old.skill_4 = skill_4
    traducteur_old.skill_5 = skill_5
    traducteur_old.skill_6 = skill_6
    traducteur_old.skill_7 = skill_7
    traducteur_old.skill_8 = skill_8
    traducteur_old.skill_9 = skill_9
    traducteur_old.skill_10 = skill_10

    traducteur_old.current_country = country
    traducteur_old.current_town = town
    traducteur_old.addr_postale = addr_postale
    traducteur_old.phone = phone
    traducteur_old.CCP_number = CCP_number
    traducteur_old.BaridiMob_RIP = BaridiMob_RIP
    traducteur_old.ePayment_type = ePayment_type
    traducteur_old.ePayment = ePayment
    traducteur_old.about_me = about_me
    traducteur_old.id_card=id_card
    traducteur_old.diploma=diploma
    traducteur_old.prestation = prestation
    traducteur_old.prestation_2 = prestation_2
    traducteur_old.prestation_3 = prestation_3
    traducteur_old.prestation_4 = prestation_4
    traducteur_old.prestation_5 = prestation_5
    traducteur_old.prestation_6 = prestation_6
    traducteur_old.prestation_7 = prestation_7

    traducteur_old.author = User.query.filter_by(id=deal.user_id).first()

    traducteur_old.caution_annual_begin = datetime.utcnow()
    traducteur_old.caution_annual_end = datetime.utcnow() + timedelta(days=365)
    traducteur_old.test_score = rate
    traducteur_old.compte_valid = True

    deal.deal_over = True
    deal.deal_over_time = datetime.utcnow()
    deal.work_score = rate

    testeur = Traducteur.query.filter_by(user_id=deal.friend_id).first()
    testeur.success_work += 1
    db.session.commit()
    
    make_payment(motif=deal.motif, amount=app.config['TESTEUR_PART'], devise=app.config['DEVISES'][0]['symbol'], eq_da=app.config['DEVISES'][0]['eq_da'], owner=deal.friend)
    this_month = Dashbord.query.filter_by(id=1).first()
    this_month.update_dashbord(freelance_part=app.config['TESTEUR_PART'], eq_da=app.config['DEVISES'][0]['eq_da'])
    
    chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==deal.user_id)) | ((Chat.user_id==deal.user_id) & (Chat.receiver_id==current_user.id))).first()
    if chat:
        chat.last_chat = datetime.utcnow()
    else:
        chat = Chat(receiver_id=deal.user_id, author=current_user)
    message = _("Votre profil de traducteur est maintenant disponible auprès des clients. Nous vous souhaitons bienvenu(e) chez %(sitname)s", sitname=app.config['SITE_NAME'])
    contact = Contact(receiver_id=deal.user_id, message=message, file_statut=False, author=current_user)
    db.session.add(contact)
    db.session.commit()
    if deal.author.last_seen + timedelta(minutes=20) < datetime.utcnow():
        subject = _('Un nouveau message')
        body = _("Depuis votre dernière visite sur TRADRDV, %(username)s vous a envoyé un nouveau message."\
            "Veuillez consulter votre messagerie.", username=current_user.username) 
        url = url_for('profile', _external=True)
        alert_email(subject, body, url, deal.author)
    return redirect(url_for('manager_panel', _external=True))


@app.route('/manager/panel')
@login_required
@check_confirmed
@check_manager
def manager_panel():
    if current_user.username is None:
        flash(_('Veuillez complèter et profiter pleinement de %(sitename)s', app.config['SITE_NAME']), 'warning')
    subtitle = _("Anonyme") if current_user.username is None else current_user.username
    # Get the deals in progress and finished for traducteur
    deals_progress = Deal.query.filter((Deal.friend_id==current_user.id) & (Deal.deal_over==False)).order_by(Deal.timestamp.desc())
    deals_over = Deal.query.filter((Deal.friend_id==current_user.id) & (Deal.deal_over==True)).order_by(Deal.timestamp.desc())
    traducteur = Traducteur.query.filter_by(user_id=current_user.id).first()

    last_deal = Deal.query.filter_by(friend_id=current_user.id).order_by(Deal.timestamp.desc()).first()
    if last_deal:
        need_help_required = True if last_deal.timestamp + timedelta(days=30) < datetime.utcnow() else False
    else:
        need_help_required = True
    return render_template('manager_panel.html', deals_progress=deals_progress.all(), deals_over=deals_over.all(), traducteur=traducteur,
        need_help_required=need_help_required, number_dp=deals_progress.count(), number_do=deals_over.count(), title=_("Profil- %(subtitle)s", subtitle=subtitle))


@app.route('/manager/action/<trad_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_manager
def manager_action(trad_id):
    name = request.form.get('name')
    statut = True if request.form.get('statut') == 'on' else False

    traducteur = Traducteur.query.filter_by(id=trad_id).first_or_404()
    if name == 'dispo':
        traducteur.dispo = statut
    elif name == 'accept_subscriber':
        traducteur.accept_subscriber = statut
    elif name == 'need_help_ad':
        if statut:
            traducteur.need_help_ad = 'ask'
        else:
            traducteur.need_help_ad = 'off'
    db.session.commit()
    return jsonify({'result': 1}), 200



@app.route('/manager/accept/<deal_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_manager
def accept_deal(deal_id):
    deal = Deal.query.filter((Deal.id==deal_id) & (Deal.friend_id==current_user.id)).first_or_404()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('manager_panel', _external=True))
    deal.friend_accept = True
    db.session.commit()
    if current_user.statut != 'testeur':
        flash(_('Vous venez d\'accepter une nouvelle commande, le temps vous est désormais compté'), 'success')
    return redirect(url_for('manager_panel', _external=True))


@app.route('/manager/reject/<deal_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_manager
def reject_deal(deal_id):
    deal = Deal.query.filter((Deal.id==deal_id) & (Deal.friend_id==current_user.id)).first_or_404()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('manager_panel', _external=True))
    traducteur = Traducteur.query.filter_by(user_id=current_user.id).first()
    deal.friend_reject = True
    deal.friend_accept = False
    traducteur.unsuccess_work += 1
    db.session.commit()    
    flash(_('Vous venez de rejeter une commande, votre statut d\'accomplissement se dégrade'), 'warning')
    return redirect(url_for('manager_panel', _external=True))


@app.route('/manager/submit/work', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_manager
def submit_work():
    deal_id = request.form.get('deal_id')
    work = request.files.get("work")

    if work:
        work.filename = secure_filename(str(datetime.timestamp(datetime.now()))+work.filename)
        work.save(os.path.join('app', 'static', 'assets', 'images', 'work_file', work.filename))
        work = os.path.join('assets', 'images', 'work_file', work.filename).replace("\\", '/')
        deal = Deal.query.filter((Deal.id==deal_id) & (Deal.friend_id==current_user.id)).first_or_404()

        if deal.deal_over is True:
            flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
            return redirect(url_for('manager_panel', _external=True))

        deal.work_did = work
        db.session.commit()
        flash(_('Félicitations, vous venez de mentionner une commande accomplie, vérification en cours'), 'success')
        return redirect(url_for('manager_panel', _external=True))
    else:
        flash(_('Veuillez joindre votre travail'), 'warning')
        return redirect(url_for('manager_panel', _external=True))


@app.route('/traducteur')
def traducteur():
    this_month = Dashbord.query.filter_by(id=1).first()
    this_month.update_dashbord(traducteur_view=1)

    page = request.args.get('page', 1, type=int)

    traducteurs = Traducteur.query.filter((Traducteur.compte_valid==True)).order_by(select_by_random())\
        .paginate(page, app.config['ORDER_PER_PAGE'], False)
    next_url = url_for('traducteur', page=traducteurs.next_num, _external=True) if traducteurs.has_next else None
    prev_url = url_for('traducteur', page=traducteurs.prev_num, _external=True) if traducteurs.has_prev else None

    return render_template('traducteur.html', traducteurs=traducteurs.items, next_url=next_url, prev_url=prev_url, page=page, 
        has_next=traducteurs.has_next, has_prev=traducteurs.has_prev, title=_('Traducteur - %(sitename)s', sitename=app.config['SITE_NAME']))


@app.route('/search/traducteur', methods=['GET', 'POST'])
def search_trad():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q')

    search = "%{}%".format(search)
    traducteurs = db.session.query(Traducteur, User).filter((User.username.like(search)) & (Traducteur.compte_valid==True))\
        .join(User, (User.id==Traducteur.user_id)).paginate(page, app.config['ORDER_PER_PAGE'], False)
    next_url = url_for('traducteur', page=traducteurs.next_num, _external=True) if traducteurs.has_next else None
    prev_url = url_for('traducteur', page=traducteurs.prev_num, _external=True) if traducteurs.has_prev else None

    return render_template('traducteur_search.html', traducteurs=traducteurs.items, next_url=next_url, prev_url=prev_url, page=page, 
        has_next=traducteurs.has_next, has_prev=traducteurs.has_prev, title=_('Traducteur- search %(search)s', search=search))


@app.route('/filter/traducteur', methods=['GET', 'POST'])
def filter_trad():
    page = request.args.get('page', 1, type=int)
    
    prestation = request.form.get('prestation')
    skill = request.form.get('skill')
    country = request.form.get('country')
    town = request.form.get('town')
    success_work = request.form.get('success_work')
    dispo = True if request.form.get('dispo') == 'on' else False
    accept_subscriber = True if request.form.get('accept_subscriber') == 'on' else False
    rate = request.form.get('rate') if not request.form.get('rate') is None else 1
    
    traducteurs = Traducteur.query.filter(
        ((Traducteur.skill_1==skill) | (Traducteur.skill_2==skill) | (Traducteur.skill_3==skill) | (Traducteur.skill_4==skill) |
        (Traducteur.skill_5==skill) | (Traducteur.skill_6==skill) | (Traducteur.skill_7==skill) | (Traducteur.skill_8==skill) |
        (Traducteur.skill_9==skill) | (Traducteur.skill_10==skill)) & (Traducteur.success_work>=success_work) & (Traducteur.dispo==dispo) & 
        (Traducteur.accept_subscriber==accept_subscriber) & (Traducteur.test_score>=rate) & ((Traducteur.prestation==prestation) | 
        (Traducteur.prestation_2==prestation) | (Traducteur.prestation_3==prestation) | (Traducteur.prestation_4==prestation) | 
        (Traducteur.prestation_5==prestation) | (Traducteur.prestation_6==prestation) | (Traducteur.prestation_7==prestation)) & 
        (Traducteur.compte_valid==True) & (Traducteur.current_country==country) & (Traducteur.current_town==town)).paginate(page, app.config['ORDER_PER_PAGE'], False)

    next_url = url_for('traducteur', page=traducteurs.next_num, _external=True) if traducteurs.has_next else None
    prev_url = url_for('traducteur', page=traducteurs.prev_num, _external=True) if traducteurs.has_prev else None

    return render_template('traducteur.html', traducteurs=traducteurs.items, next_url=next_url, prev_url=prev_url, page=page, 
        has_next=traducteurs.has_next, has_prev=traducteurs.has_prev, title=_('Traducteur- filter %(skill)s', skill=skill))


@app.route('/traducteur/single/<trad_id>', methods=['GET', 'POST'])
def traducteur_single(trad_id):
    traducteur = Traducteur.query.filter((Traducteur.id==trad_id) & (Traducteur.compte_valid==True)).first_or_404()
    traducteur.add_view()
    return render_template('single_traducteur.html', traducteur=traducteur, title=_('Traducteur profil- %(username)s', username=traducteur.author.username))


@app.route('/contact/traducteur/<trad_id>', methods=['POST', 'GET'])
@login_required
@check_confirmed
def contact_trad(trad_id):
    traducteur = Traducteur.query.filter((Traducteur.id==trad_id) & (Traducteur.compte_valid==True)).first_or_404()
    if traducteur.user_id == current_user.id:
        flash(_('Vous ne pouvez pas contacter vous même'), 'warning')
        return redirect(url_for('profile', _external=True))
    chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==traducteur.user_id)) |\
            ((Chat.user_id==traducteur.user_id) & (Chat.receiver_id==current_user.id))).first()
    if chat:
        chat.last_chat = datetime.utcnow()
    else:
        chat = Chat(receiver_id=traducteur.user_id, author=current_user)
    message = _("Nouveau message, je suis intéressé par votre profil. Etes vous disponible pour me renseigner?")
    contact = Contact(receiver_id=traducteur.user_id, message=message, file_statut=False, author=current_user)
    db.session.add(contact)
    db.session.commit()
    if traducteur.author.last_seen + timedelta(minutes=20) < datetime.utcnow():
        subject = _('Un nouveau message')
        body = _('Depuis votre dernière visite sur TRADRDV, %(username)s aimerait entrer en contact avec vous.\
                Veuillez consulter votre messagerie.', username=current_user.username) 
        url = url_for('profile', _external=True)
        alert_email(subject, body, url, traducteur.author)
        return redirect(url_for('profile', _external=True))
    flash(_('Veuillez cliquer sur le pseudo du prestataire dans la discussion pour entamer la conversation'), 'success')
    return redirect(url_for('profile', _external=True))


@app.route('/traducteur/hire', methods=['GET', 'POST'])
@login_required
@check_confirmed
def trad_hire():
    payment_way = request.form.get('payment_way')
    trad_id = request.form.get('trad_id')
    motif = request.form.get('motif')
    amount = request.form.get('amount')
    devise = request.form.get('devise')

    if payment_way == 'abonnement':
        if current_user.offre_statut == 'gratuit':
            flash(_('Vous n\'avez aucune offre active. Veuillez vous abonner avant d\'utiliser cette option'), 'warning')
            return redirect(url_for('accueil', _external=True))
        elif current_user.daily_offer==0:
            flash(_('Vous avez déjà utilisé l\'offre journalière de votre abonnement. Veuillez payer cash ou attendez le prochain 00 heure'), 'warning')
            return redirect(url_for('accueil', _external=True))

    traducteur = Traducteur.query.filter((Traducteur.id==trad_id) & (Traducteur.compte_valid==True)).first_or_404()
    if traducteur.user_id == current_user.id:
        flash(_('Vous ne pouvez pas engager vous même'), 'warning')
        return redirect(url_for('profile', _external=True))

    if payment_way == 'abonnement':
        deal = Deal(type_deal='trad', payment_way=payment_way, motif=motif, amount=0, admin_confirm_bill=True, bill_is_added=True,
            devise=devise, friend=traducteur.author, author=current_user)
    elif payment_way == 'cash':
        deal = Deal(type_deal='trad', payment_way=payment_way, motif=motif, amount=amount, devise=devise, friend=traducteur.author, author=current_user)
    else:
        return render_template('404.html', title=_("404 Erreur")), 404
    current_user.daily_offer = 0
    db.session.add(deal)
    db.session.commit()
    return redirect(url_for('profile', _external=True))


@app.route('/get/town', methods=['GET', 'POST'])
def get_town():
    country = request.form.get('country')
    towns = app.config["TOWNS"][country]
    return jsonify({'towns': towns}), 200


@app.route('/get/testeur', methods=['GET', 'POST'])
def get_testeur():
    testeur_id = request.form.get('testeur_id')
    testeur = Traducteur.query.filter_by(user_id=testeur_id).first()
    return jsonify({'testeur': testeur.as_dict()}), 200




# -------------------------------------------------#
#-------Deal route treatement program--------#
#--------------------------------------------------#
@app.route('/deal/submit/bill', methods=['POST', 'GET'])
@login_required
@check_confirmed
def deal_submit_bill():
    deal_id = request.form.get('deal_id')
    motif_update = request.form.get('motif_update')
    amount_update = request.form.get('amount_update')
    payment_bill = request.files.get("payment_bill")
    
    deal = Deal.query.filter_by(id=deal_id).first()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('profile', _external=True))
    if deal.friend_accept is False:
        flash(_('Attendez l\'avis du prestataire avant de joindre le reçu'), 'warning')
        return redirect(url_for('profile', _external=True))

    if payment_bill:
        if allowed_image(payment_bill.filename):
            payment_bill.filename = secure_filename(str(datetime.timestamp(datetime.now()))+payment_bill.filename)
            Image.open(payment_bill).resize((500, 500)).save(os.path.join('app', 'static', 'assets', 'images', 'bill_img', payment_bill.filename))
            payment_bill = os.path.join('assets', 'images', 'bill_img', payment_bill.filename).replace("\\", '/')
        else:
            flash(_('Erreur de nom ou d\'extension du carte identité/passeport'), 'danger')
            return redirect(url_for('profile', _external=True))
    else:
        payment_bill = None

    if deal.friend_accept is False:
        deal.motif = motif_update if not motif_update is None else deal.motif
        deal.amount = amount_update if not amount_update is None else deal.amount
    if deal.admin_confirm_bill is False:
        deal.payment_bill = payment_bill if not payment_bill is None else deal.payment_bill
        if not payment_bill is None:
            deal.bill_is_added = True
        db.session.commit()
    return redirect(url_for('profile', _external=True))


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
        message = _("Nouveau contact")
        contact = Contact(receiver_id=admin.id, message=message, file_statut=False, author=current_user)
        db.session.add(contact)
        db.session.commit()
        if admin.last_seen + timedelta(minutes=20) < datetime.utcnow():
            subject = _('Un nouveau message')
            body = _('Depuis votre dernière visite sur TRADRDV, %(username)s aimerait entrer en contact avec vous.\
                Veuillez consulter votre messagerie.', username=current_user.username) 
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
            msg_file.save(os.path.join('app', 'static', 'assets', 'images', 'message_file', msg_file.filename))
            msg_file = os.path.join('assets', 'images', 'message_file', msg_file.filename).replace("\\", '/')
            
            contact = Contact(receiver_id=receiver_id, file=msg_file, file_statut=file_statut, author=current_user)
            db.session.add(contact)
            db.session.commit()
        else:
            contact = Contact(receiver_id=receiver_id, message=msg_text, author=current_user)
            db.session.add(contact)
            db.session.commit()
        if user.last_seen + timedelta(minutes=20) < datetime.utcnow():
            subject = _('Un nouveau message')
            body = _('Depuis votre dernière visite sur TRADRDV, %(username)s vous a envoyé un message.\
                Veuillez consulter votre messagerie.', username=current_user.username) 
            url = url_for('profile', _external=True)
            alert_email(subject, body, url, user)      
    return jsonify({}), 200


@app.route('/get/message', methods=['GET', 'POST'])
@login_required
@check_confirmed
def get_message():
    receiver_id = request.form.get('receiver_id')
    chats = Chat.query.filter((Chat.user_id==current_user.id) | (Chat.receiver_id==current_user.id)).order_by(Chat.last_chat.desc()).all()
    chats = [chat.as_dict() for chat in chats]
    user = User.query.filter_by(id=current_user.id).first()

    if receiver_id == '':
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


@app.route('/newsletter/send', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def send_newsletter():
    group=request.form.get('group')
    url=request.form.get('url')
    subject=request.form.get('subject')
    message=request.form.get('message')

    emails = []  
    if group == 'Groupe particulier':
        followers = Newsletter.query.all()
        emails = [follower.email for follower in followers]
        newsletter_email(emails, subject, message, url)
    
    elif group == 'Groupe client':
        clients = User.query.filter_by(statut='client').all()
        emails = [client.email for client in clients]
        newsletter_email(emails, subject, message, url)
    
    elif group == 'Groupe traducteur':
        traducteurs = User.query.filter_by(statut='traducteur').all()
        emails = [traducteur.email for traducteur in traducteurs]
        newsletter_email(emails, subject, message, url)
    
    elif group == 'Groupe testeur':
        testeurs = User.query.filter_by(statut='testeur').all()
        emails = [testeur.email for testeur in testeurs]
        newsletter_email(emails, subject, message, url)
    
    elif group == 'Groupe admin':
        admins = User.query.filter_by(statut='admin').all()
        emails = [admin.email for admin in admins]
        newsletter_email(emails, subject, message, url)
    flash(_('Le broadcast est envoyé'), 'success')
    return redirect(url_for('admin_panel', _external=True))


# -------------------------------------------------#
#-------Admin route treatement program-------------#
#--------------------------------------------------#
@app.route('/admin/panel')
@login_required
@check_confirmed
@check_admin
def admin_panel():
    if current_user.username is None:
        flash(_('Veuillez complèter et profiter pleinement de %(sitename)s', app.config['SITE_NAME']), 'warning')
    subtitle = _("Anonyme") if current_user.username is None else current_user.username
    
    deals_progress = Deal.query.filter((Deal.friend_accept==True) & (Deal.deal_over==False) & (Deal.work_did!=None)).order_by(Deal.timestamp.desc())
    deals_over = Deal.query.filter_by(deal_over=True).order_by(Deal.timestamp.desc())
    deals_reject = Deal.query.filter((Deal.friend_reject==True) & (Deal.deal_over==False)).order_by(Deal.timestamp.desc())
    deals_check_bill = Deal.query.filter((Deal.admin_confirm_bill==False) & (Deal.bill_is_added==True) & (Deal.deal_over==False)).order_by(Deal.timestamp.desc())
    traducteurs_need_ad = Traducteur.query.filter((Traducteur.compte_valid==True) & ((Traducteur.need_help_ad=='on') | (Traducteur.need_help_ad=='ask')))\
        .order_by(select_by_random()).all()

    #Number of .....
    number_client = User.query.filter_by(statut='client').count()
    number_traducteur = User.query.filter_by(statut='traducteur').count()
    number_testeur = User.query.filter_by(statut='testeur').count()
    number_admin = User.query.filter_by(statut='admin').count()
    number_newsletter = Newsletter.query.count()
    number_pub = Pub.query.filter_by(valid=True).count()
    number_pub_sub = Marketing.query.filter_by(compte_valid=True).count()
    #List of traducteur to select for reject deal
    list_trad = Traducteur.query.filter((Traducteur.compte_valid==True)).all()
    #Dashbord of the two months
    dashbord_this_month = Dashbord.query.filter_by(id=1).first()
    dashbord_last_month = Dashbord.query.filter_by(id=2).first()

    #Profile
    clients = User.query.filter_by(statut='client').all()
    traducteurs = Traducteur.query.all()

    return render_template('admin_panel.html', deals_progress=deals_progress.all(), deals_over=deals_over.all(), deals_reject=deals_reject.all(), 
        deals_check_bill=deals_check_bill.all(), list_trad=list_trad, number_client=number_client, number_traducteur=number_traducteur, 
        number_testeur=number_testeur, number_admin=number_admin, number_newsletter=number_newsletter, number_dp=deals_progress.count(), number_do=deals_over.count(), 
        number_dr=deals_reject.count(), number_dcb=deals_check_bill.count(), dashbord_this_month=dashbord_this_month, dashbord_last_month=dashbord_last_month, 
        traducteurs_need_ad=traducteurs_need_ad, clients=clients, traducteurs=traducteurs, number_pub=number_pub, number_pub_sub=number_pub_sub, title=_("Profil- %(subtitle)s", subtitle=subtitle))


@app.route('/admin/submit/checked/work', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def submit_checked_work():
    deal_id = request.form.get('deal_id')
    rate = request.form.get('rate') if not request.form.get('rate') is None else 1
    checked_work = request.files.get("checked_work")

    deal = Deal.query.filter((Deal.id==deal_id)).first_or_404()
    traducteur = Traducteur.query.filter_by(user_id=deal.friend_id).first()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('admin_panel', _external=True))

    if checked_work:
        checked_work.filename = secure_filename(str(datetime.timestamp(datetime.now()))+checked_work.filename)
        checked_work.save(os.path.join('app', 'static', 'assets', 'images', 'work_file', checked_work.filename))
        checked_work = os.path.join('assets', 'images', 'work_file', checked_work.filename).replace("\\", '/')

        deal.work_valid = checked_work
        deal.work_score = rate
        deal.deal_over = True
        deal.deal_over_time = datetime.utcnow()
        traducteur.success_work += 1 
    
        this_month = Dashbord.query.filter_by(id=1).first()
        if deal.payment_way == 'cash':
            make_payment(motif=deal.motif, amount=(deal.amount*app.config['TRAD_PART_NO_ABON'])/100, devise=deal.devise, eq_da=return_eq_da(deal.devise), owner=deal.friend)
            this_month.update_dashbord(freelance_part=(deal.amount*app.config['TRAD_PART_NO_ABON'])/100, eq_da=return_eq_da(deal.devise))
        elif deal.payment_way == 'abonnement':
            make_payment(motif=deal.motif, amount=app.config['TRAD_PART_ABON'], devise=deal.devise, eq_da=return_eq_da(deal.devise), owner=deal.friend)
            this_month.update_dashbord(freelance_part=app.config['TRAD_PART_ABON'], eq_da=return_eq_da(deal.devise))

        # Deal is over text from traductor to custom
        chat = Chat.query.filter(((Chat.user_id==deal.friend_id) & (Chat.receiver_id==deal.user_id)) |\
            ((Chat.user_id==deal.user_id) & (Chat.receiver_id==deal.friend_id))).first()
        if chat:
            chat.last_chat = datetime.utcnow()
        else:
            chat = Chat(receiver_id=deal.user_id, author=deal.friend)
        message = _("ACCORD TERMINE: merci d'avoir choisi %(site_name)s", site_name=app.config['SITE_NAME'])
        contact = Contact(receiver_id=deal.user_id, message=message, file_statut=False, author=deal.friend)
        db.session.add(contact)
        db.session.commit()
        if deal.author.last_seen + timedelta(minutes=20) < datetime.utcnow():
            subject = _('Un nouveau message')
            body = _('Depuis votre dernière visite sur TRADRDV, %(username)s vous a laissé(e) un message.\
                Veuillez consulter votre messagerie.', username=deal.author.username) 
            url = url_for('profile', _external=True)
            alert_email(subject, body, url, deal.author)
        
        # Congrat text from admin to traducteur
        chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==deal.friend_id)) |\
            ((Chat.user_id==deal.friend_id) & (Chat.receiver_id==current_user.id))).first()
        if chat:
            chat.last_chat = datetime.utcnow()
        else:
            chat = Chat(receiver_id=deal.friend_id, author=current_user)
        message = _("Félicitations pour votre nouveau point d’expérience, continuez de gravir les échelons, y’en aura encore !")
        contact = Contact(receiver_id=deal.friend_id, message=message, file_statut=False, author=current_user)
        db.session.add(contact)
        db.session.commit()
        if deal.friend.last_seen + timedelta(minutes=20) < datetime.utcnow():
            subject = _('Un nouveau message')
            body = _('Depuis votre dernière visite sur TRADRDV, %(username)s vous a laissé(e) un message.\
                Veuillez consulter votre messagerie.', username=current_user.username) 
            url = url_for('profile', _external=True)
            alert_email(subject, body, url, deal.author)

        flash(_('Commande terminée'), 'success')
        return redirect(url_for('admin_panel', _external=True))
    else:
        flash(_('Veuillez joindre un fichier'), 'warning')
        return redirect(url_for('admin_panel', _external=True))


@app.route('/admin/valid/bill/<deal_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def valid_deal_bill(deal_id):
    deal = Deal.query.filter((Deal.id==deal_id)).first_or_404()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('manager_panel', _external=True))
    deal.admin_confirm_bill = True
    db.session.commit()

    make_payment(motif=deal.motif, amount=-deal.amount, devise=deal.devise, eq_da=return_eq_da(deal.devise), owner=deal.author)
    this_month = Dashbord.query.filter_by(id=1).first()
    if deal.type_deal == 'test':
        this_month.update_dashbord(revenu_test=deal.amount, eq_da=return_eq_da(deal.devise))
    elif deal.type_deal == 'trad':
        this_month.update_dashbord(revenu_work=deal.amount, eq_da=return_eq_da(deal.devise))

    flash(_('La conformité et l\'originalité du reçu confirmées'), 'success')
    return redirect(url_for('admin_panel', _external=True))


@app.route('/admin/reject/bill/<deal_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def reject_deal_bill(deal_id):
    deal = Deal.query.filter((Deal.id==deal_id)).first_or_404()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('manager_panel', _external=True))

    chat = Chat.query.filter(((Chat.user_id==current_user.id) & (Chat.receiver_id==deal.user_id)) |\
            ((Chat.user_id==deal.user_id) & (Chat.receiver_id==current_user.id))).first()
    if chat:
        chat.last_chat = datetime.utcnow()
    else:
        chat = Chat(receiver_id=deal.user_id, author=current_user)
    message = _("Désolé, votre reçu n'est pas vérifié. Veuillez nous envoyer plus de détails par la discussion")
    contact = Contact(receiver_id=deal.user_id, message=message, file_statut=False, author=current_user)
    db.session.add(contact)
    db.session.commit()
    if deal.author.last_seen + timedelta(minutes=20) < datetime.utcnow():
        subject = _('Un nouveau message')
        body = _('Depuis votre dernière visite sur TRADRDV, %(username)s vous a laissé(e) un message.\
                Veuillez consulter votre messagerie.', username=current_user.username) 
        url = url_for('profile', _external=True)
        alert_email(subject, body, url, deal.author)

    flash(_('La conformité et l\'originalité du reçu rejetées'), 'success')
    return redirect(url_for('admin_panel', _external=True))


@app.route('/admin/attribute/new_trad', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def attribute_new_trad():
    deal_id = request.form.get('deal_id')
    trad_id = request.form.get('trad_id')

    deal = Deal.query.filter((Deal.id==deal_id)).first_or_404()
    friend = User.query.filter_by(id=trad_id).first()
    author = User.query.filter_by(id=deal.user_id).first()

    deal.friend=friend
    deal.author=author
    deal.friend_accept=False
    deal.friend_reject=False
    db.session.commit()

    chat = Chat.query.filter(((Chat.user_id==friend.id) & (Chat.receiver_id==author.id)) | ((Chat.user_id==author.id) & (Chat.receiver_id==friend.id))).first()
    if chat:
        chat.last_chat = datetime.utcnow()
    else:
        chat = Chat(receiver_id=author.id, author=friend)
    message = _("Bonjour, je suis votre nouveau prestataire sur l'accord: %(motif)s", motif=deal.motif)
    contact = Contact(receiver_id=author.id, message=message, file_statut=False, author=friend)
    db.session.add(contact)
    db.session.commit()
    if author.last_seen + timedelta(minutes=20) < datetime.utcnow():
        subject = _('Un nouveau message')
        body = _("Depuis votre dernière visite sur TRADRDV, %(username)s un nouveau prestataire a repris votre accord suite au refus de l'autre. "\
            "Veuillez consulter votre messagerie.", username=friend.username) 
        url = url_for('profile', _external=True)
        alert_email(subject, body, url, author)
    return redirect(url_for('admin_panel', _external=True))


@app.route('/admin/enroll/offer/<deal_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def enroll_offer(deal_id):
    deal = Deal.query.filter((Deal.id==deal_id)).first_or_404()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('admin_panel', _external=True))
    deal.admin_confirm_bill = True
    deal.work_score = 5
    deal.deal_over = True
    deal.deal_over_time = datetime.utcnow()
    db.session.commit()
    
    user = User.query.filter_by(id=deal.user_id).first()  
    if deal.amount == app.config['OFFRE_STATUTS']['standard']['price_da']:
        user.offre_statut = 'standard'
        user.offre_begin = datetime.utcnow()
        user.offre_end = datetime.utcnow() + timedelta(days=182)
        db.session.commit()
    if deal.amount == app.config['OFFRE_STATUTS']['premium']['price_da']:
        user.offre_statut = 'premium'
        user.offre_begin = datetime.utcnow()
        user.offre_end = datetime.utcnow() + timedelta(days=365)
        db.session.commit()
    
    make_payment(motif=deal.motif, amount=-deal.amount, devise=deal.devise, eq_da=return_eq_da(deal.devise), owner=deal.author)
    this_month = Dashbord.query.filter_by(id=1).first()
    this_month.update_dashbord(revenu_abon=deal.amount, eq_da=return_eq_da(deal.devise))

    flash(_('La conformité et l\'originalité du reçu confirmées'), 'success')
    return redirect(url_for('admin_panel', _external=True))


@app.route('/admin/pub/offer', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def pub_offer():
    deal_id = request.form.get('deal_id')
    nbr_pub = request.form.get('nbr_pub')
    days = request.form.get('days')
    deal = Deal.query.filter((Deal.id==deal_id)).first_or_404()
    if deal.deal_over is True:
        flash(_('Cet accord est terminé le %(date)s', date=deal.deal_over_time.strftime("%m/%d/%Y, %H:%M")), 'warning')
        return redirect(url_for('admin_panel', _external=True))
    deal.admin_confirm_bill = True
    deal.work_score = 5
    deal.deal_over = True
    deal.deal_over_time = datetime.utcnow()
    db.session.commit()
    
    account = Marketing.query.filter_by(user_id=deal.user_id).first()  
    account.caution_begin = datetime.utcnow()
    account.caution_end = datetime.utcnow() + timedelta(days=int(days))
    account.nbr_pub = int(nbr_pub)
    account.compte_valid = True
    db.session.commit()
    
    make_payment(motif=deal.motif, amount=-deal.amount, devise=deal.devise, eq_da=return_eq_da(deal.devise), owner=deal.author)
    this_month = Dashbord.query.filter_by(id=1).first()
    this_month.update_dashbord(revenu_abon=deal.amount, eq_da=return_eq_da(deal.devise))

    flash(_('La conformité et l\'originalité du reçu confirmées'), 'success')
    return redirect(url_for('admin_panel', _external=True))


@app.route('/admin/boost/<trad_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def admin_boost(trad_id):
    statut = True if request.form.get('statut') == 'on' else False

    traducteur = Traducteur.query.filter_by(id=trad_id).first_or_404()
    if statut:
        traducteur.need_help_ad = 'on'
    else:
        traducteur.need_help_ad = 'off'
    db.session.commit()
    return jsonify({'result': 1}), 200


@app.route('/admin/get/profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def admin_get_profile():
    id = request.form.get('id')
    type_profile = request.form.get('type_profile')

    if type_profile == 'client':
        client = User.query.filter_by(id=id).first()
        login_url = url_for('admin_login', id=client.id, _external=True)
        data = client.as_dict()
    elif type_profile == 'traducteur':
        traducteur = Traducteur.query.filter_by(id=id).first()
        login_url = url_for('admin_login', id=traducteur.user_id, _external=True)
        data = traducteur.as_dict()

    return jsonify({'data': data, 'type_profile': type_profile, 'login_url': login_url}), 200


@app.route('/admin/login/<id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def admin_login(id):
    user = User.query.filter_by(id=id).first_or_404()
    login_user(user, remember=False)
    return redirect(url_for('profile', _external=True))


@app.route('/admin/pay/traducteur', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_admin
def admin_pay_trad():
    trad_id = request.form.get('trad_id')
    motif = request.form.get('motif')
    amount = int(request.form.get('amount'))
    devise = request.form.get('devise')

    traducteur = Traducteur.query.filter((Traducteur.id==trad_id)).first_or_404()
    user = User.query.filter_by(id=traducteur.user_id).first()
    if user:
        if user.revenu >= amount:
            get_paid(motif=motif, amount=amount, devise=devise, eq_da=return_eq_da(devise), owner=user)
            subject = motif
            body = _("Depuis votre dernière visite sur TRADRDV, vous avez reçu un salaire mensuel de %(amount)s %(devise)s de la part de TRADRDV. "\
                "Veuillez consulter votre compte en banque.", amount=amount, devise=devise) 
            url = url_for('profile', _external=True)
            alert_email(subject, body, url, user)
            flash(_('Paiement effectué'), 'success')
        else:
            flash(_('Erreur de paiement, le revenu du traducteur est insuffisant'), 'warning')
    return redirect(url_for('admin_panel', _external=True))


# -------------------------------------------------#
#-------Other route treatement program-------------#
#--------------------------------------------------#
@app.route('/get/notification', methods=['GET', 'POST'])
@login_required
@check_confirmed
def get_notification():
    number_new_msg = Contact.query.filter_by(read=False).count()
    return jsonify({'number_new_msg':number_new_msg}), 200


@app.route('/news')
@in_development
def news():
    return render_template('news.html', title=_('Articles-%(sitename)s', sitename=app.config['SITE_NAME']))


@app.route('/about_us')
def about_us():
    return render_template('about.html', title=_('À Propos de nous'))


@app.route('/terms')
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