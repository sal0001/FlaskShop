from loja import db
from flask_bcrypt import generate_password_hash

class Utilizador(db.Model):
    __tablename__ = 'utilizadores'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    cliente = db.relationship('Cliente', backref='utilizador', uselist=False)

    def get_id(self):
        return str(self.id)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True     
    def __repr__(self):
        return '< Utilizador %r>' % self.email

    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)  

    def __repr__(self):
        return f'<Role {self.descricao}>'

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    morada = db.Column(db.String(100))
    utilizadorId = db.Column(db.Integer, db.ForeignKey('utilizadores.id'))

    def __repr__(self):
        return f"< Cliente {self.id}: {self.nome}>"
    

if __name__ == "__main__":
    db.create_all()
