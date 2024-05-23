from loja import db


class Encomenda(db.Model):
    __tablename__ = 'encomendas'

    id = db.Column(db.Integer, primary_key=True)
    clienteId = db.Column(db.Integer, nullable=True)
    dataEncomenda = db.Column(db.Date, nullable=True)
    total = db.Column(db.Float, nullable=True)

    linhas_encomenda = db.relationship('LinhaEncomenda', backref='encomenda', lazy=True)

class LinhaEncomenda(db.Model):
    __tablename__ = 'linhas_encomenda'

    id = db.Column(db.Integer, primary_key=True)
    encomendaId = db.Column(db.Integer, db.ForeignKey('encomendas.id'))  
    produtoId = db.Column(db.Integer, db.ForeignKey('produtos.id'))  
    quantidade = db.Column(db.Integer, nullable=True)


    produto = db.relationship('Produto', backref='linhas_encomenda', lazy=True)
        
if __name__ == "__main__":
    db.create_all()