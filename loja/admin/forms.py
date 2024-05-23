from wtforms import StringField, PasswordField, validators, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from flask_wtf import FlaskForm
from .models import Utilizador

class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    morada = StringField('Morada', validators=[DataRequired()])
    roleId = IntegerField('roleId', default=2)
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),  
        validators.Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]+$",
            message="A senha deve conter pelo menos uma letra minúscula, uma letra maiúscula, um número e um caractere especial."
        )
    ])
    def validate_email(self, email):
        existing_user = Utilizador.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('Email já está em uso. Por favor, escolha outro.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
