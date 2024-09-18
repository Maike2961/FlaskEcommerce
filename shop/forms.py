from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from shop.models import User


class CadastroForm(FlaskForm):
    usuario = StringField(label='Username: ', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='E-mail: ', validators=[Email(), DataRequired()])
    senha1 = PasswordField(label='Senha: ', validators=[Length(min=6), DataRequired()])
    senha2 = PasswordField(label='Confirmação de senha: ', validators=[EqualTo('senha1'), DataRequired()])
    submit = SubmitField(label='Cadastrar')
    
    def validate_usuario(self, check_user):
        user = User.query.filter_by(usuario=check_user.data).first()
        print(check_user.data)
        if user:
            raise ValidationError("Usuario já existe! Cadastro outro nome de usuário")
        
    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        print(check_email.data)
        if email:
            raise ValidationError('E-mail ja existe, Cadastre outro')
        
    def validate_senha1(self, check_senha):
        senha = User.query.filter_by(senha=check_senha.data).first()
        if senha:
            raise ValidationError("Senha já existe! Cadastre outra senha")
        
        
class LoginForm(FlaskForm):
    usuario = StringField(label='Usuario', validators=[DataRequired()])
    senha = StringField(label='Senha', validators=[DataRequired()])
    submit = SubmitField(label='Log In')
    
    
class ComprarProdutoForm(FlaskForm):
    submit = SubmitField(label="Comprar Produto")
    
    
class VenderProdutoForm(FlaskForm):
    submit = SubmitField(label="Vender Produto")
    