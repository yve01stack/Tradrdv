from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    email = StringField(_l('E-mail'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Mot de passe'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Rappelez-vous de moi'))
    submit = SubmitField(_l('Se connecter'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Pseudonyme'), validators=[DataRequired()])
    fullname = StringField(_l('Nom complet'), validators=[DataRequired()])
    email = StringField(_l('E-mail'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Mot de passe'), validators=[DataRequired()])
    password2 = PasswordField(_l('Confirmer le mot de passe'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('S\'inscrire'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Veuillez utiliser un pseudonyme différent.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Veuillez utiliser une adresse e-mail différente.'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Demande'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Nouveau mot de passe'), validators=[DataRequired()])
    password2 = PasswordField(_l('Confirmer'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Réinitialiser'))