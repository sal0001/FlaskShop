from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, FileField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from .models import Categoria

class ProdutoForm(FlaskForm):
    descricao = StringField(validators=[InputRequired()])
    preco = FloatField('Preço', validators=[InputRequired()])
    image_url = FileField('Imagem', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    categoria_id = SelectField('Categoria', coerce=int)

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.categoria_id.choices = [(categoria.id, categoria.descricao) for categoria in Categoria.query.all()]
        
class CategoriaForm(FlaskForm):
    descricao = StringField('Descrição', validators=[InputRequired()])
