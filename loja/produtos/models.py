
from loja import db



class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column('id', db.Integer, primary_key=True)
    descricao = db.Column('descricao', db.String(100), nullable=False)
    preco = db.Column('preco', db.Float, nullable=False)
    image_url = db.Column('image_url', db.String(150), nullable=False) 
    categoriaId = db.Column('categoriaId', db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('produtos', lazy=True))

    def __repr__(self):
        return '<Produto %r>' % self.descricao

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(250), nullable=True)
    
    def __repr__(self):
        return '<Categoria %r>' % self.descricao

if __name__ == "__main__":
    db.create_all()