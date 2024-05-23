from flask import render_template, session, url_for, flash, redirect, request, render_template_string, jsonify
from flask_login import login_user
from loja import app, db, login_manager, mail, bcrypt
from loja.admin.forms import RegistrationForm, LoginForm
from loja.admin.models import Utilizador, Cliente
from loja.produtos.models import Produto
from functools import wraps
from flask_mail import Message
from flask_login import current_user
from datetime import date
from loja.carrinho.models import LinhaEncomenda, Encomenda



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:   
            flash('Por favor, faça o login para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.roleId == 1:
            flash('Nao tem permissao para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def client_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.roleId == 2:
            flash('Nao tem permissao para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return Utilizador.query.get(int(user_id))


def already_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.roleId == 1:
                return redirect(url_for('admin'))
            elif current_user.roleId == 2:
                return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def layout():
    return render_template("layout.html")

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/home')
@client_user
@login_required
def home():
        return render_template('cliente/home.html')


@app.route('/admin')
@login_required
@admin_user
def admin():
    produtos = Produto.query.all()
    return render_template("admin/index.html", produtos=produtos)


@app.route('/registar', methods=['GET', 'POST'])
@already_login
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        nome = form.nome.data
        morada = form.morada.data 
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        existing_user = Utilizador.query.filter_by(email=email).first()
        if existing_user:
            flash('Email já está em uso. Por favor, escolha outro.', 'error')
            return redirect(url_for('register'))

        novo_utilizador = Utilizador(email=email, password=hashed_password, roleId=2)
        db.session.add(novo_utilizador)
        db.session.commit()

        novo_cliente = Cliente(nome=nome, morada=morada, utilizadorId=novo_utilizador.id)
        db.session.add(novo_cliente)
        db.session.commit()

        flash('Registo bem-sucedido! Faça o login para continuar.', 'success')
        return redirect(url_for('login'))
    return render_template('admin/registar.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
@already_login
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data

        utilizador = Utilizador.query.filter_by(email=email).first()

        if utilizador and bcrypt.check_password_hash(utilizador.password, form.password.data):
            login_user(utilizador)
            if utilizador.roleId == 1:
                return redirect(url_for('admin')) 
            else:
                return redirect(url_for('home')) 
        else:
            flash('Email não encontrado ou senha incorreta. Por favor, tente novamente.', 'danger')
    return render_template('admin/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('layout'))

@app.route('/profile')
@client_user
def profile():
    cliente_id = current_user.id  
    return render_template('cliente/profile.html', cliente_id=cliente_id)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/removecliente/<int:id>', methods=['POST'])
@login_required
@admin_user
def removecliente(id):
    cliente = Cliente.query.get_or_404(id)
    utilizador = Utilizador.query.filter_by(id=cliente.utilizadorId).first()
    if utilizador:
        db.session.delete(utilizador)
    db.session.delete(cliente)
    db.session.commit()
    flash(f'{cliente.nome} removido com sucesso', 'success')  
    return redirect(url_for('clientes'))



@app.route("/clientes")
@admin_user
@login_required
def clientes():
    clientes = Cliente.query.all()
    return render_template('cliente/clientes.html', clientes=clientes)


@app.route('/add_carrinho/<int:produto_id>', methods=['POST'])
@login_required
def add_carrinho(produto_id):
    produto = Produto.query.get(produto_id)
    if produto:
        if 'carrinho' not in session or not isinstance(session['carrinho'], dict):
            session['carrinho'] = {}

        carrinho = session['carrinho']

        if produto_id in carrinho:
            carrinho[produto_id] += 1
        else:
            carrinho[produto_id] = 1
            flash("Produto adicionado ao carrinho", "success")
            
        session['carrinho'] = carrinho

    return redirect(url_for('produto', produto_id=produto_id))



@app.route('/update_cart/<int:produto_id>', methods=['POST'])
@login_required
def update_cart(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        flash("Produto não encontrado", "danger")
        return redirect(url_for('carrinho'))
    
    data = request.get_json()
    new_quantity = data.get('quantity', 0)
    
    if new_quantity < 0:
        flash("Quantidade inválida", "danger")
        return redirect(url_for('carrinho'))
    
    if 'carrinho' not in session or not isinstance(session['carrinho'], dict):
        session['carrinho'] = {}

    carrinho = session['carrinho']
    
    if produto_id in carrinho:
       
        carrinho[produto_id] = new_quantity
    
    session['carrinho'] = carrinho
    
 
    total_produto = produto.preco * new_quantity

    total_carrinho = sum(produto.preco * quantity for produto_id, quantity in carrinho.items())

    return jsonify({'total_produto': total_produto, 'total_carrinho': total_carrinho})


@app.route('/carrinho')
@login_required
def carrinho():
    carrinho_ids = session.get('carrinho', {})
    produtos = []
    total_carrinho = 0
    for produto_id, quantity in carrinho_ids.items():
        produto = Produto.query.get(produto_id)
        if produto:
            produtos.append((produto, quantity))
            total_carrinho += produto.preco * quantity

    quantidade_total = sum(carrinho_ids.values()) 

    cliente_id = current_user.id
    return render_template('carrinho/carrinho.html', produtos=produtos, total_carrinho=total_carrinho, quantidade_total=quantidade_total, cliente_id=cliente_id)


@app.route('/remover_do_carrinho/<int:produto_id>', methods=['POST'])
@login_required
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', {})
    if produto_id in carrinho:
        del carrinho[produto_id]
        flash("Produto removido do carrinho", "success")
    else:
        flash("Produto não encontrado no carrinho", "danger")
    
    session['carrinho'] = carrinho
    return redirect(url_for('carrinho'))


@app.route('/finalizar_encomenda', methods=['POST'])
@login_required
@client_user
def finalizar_encomenda():
    cliente_id = current_user.id

  
    carrinho = session.get('carrinho', {})
    if not carrinho:  
        flash("Adicione produtos ao carrinho para finalizar", "danger")
        return redirect(url_for('carrinho'))


    total_encomenda = sum(Produto.query.get(produto_id).preco * quantidade for produto_id, quantidade in carrinho.items())

 
    nova_encomenda = Encomenda(clienteId=cliente_id, dataEncomenda=date.today(), total=total_encomenda)
    db.session.add(nova_encomenda)


    total_produto_string = ""
    for produto_id, quantidade in carrinho.items():
        produto = Produto.query.get(produto_id)
        if produto:
            linha_encomenda = LinhaEncomenda(encomendaId=nova_encomenda.id, produtoId=produto_id, quantidade=quantidade)
            db.session.add(linha_encomenda)
            total_produto_string += f"\n- Produto: {produto.descricao}\n  - Quantidade: {quantidade}\n  - Preço unitário: {produto.preco}€\n---------------------------------------------------\n"

    db.session.commit()


    email_cliente = current_user.email
    if email_cliente:
        email_corpo = render_template_string(
            """\
            Olá,

            A sua encomenda foi concluída com sucesso! Aqui estão os detalhes:
            {{ total_produto_string }}
            - Total: {{ total_encomenda }}€
            Envie o pagamento para a seguinte referencia: PT50000749138950121151585
            Obrigado por fazer negócios conosco!
            """,
            total_produto_string=total_produto_string,
            total_encomenda=total_encomenda
        )
            
        msg = Message(subject="Encomenda Concluída", sender='aluno222062@epad.edu.pt', recipients=[email_cliente], body=email_corpo)
        mail.send(msg)
        flash('Verifique o seu email!', 'success')
    else:
        flash('Não foi possível encontrar o email do cliente.', 'danger')

    session.pop('carrinho', None)

    return redirect(url_for('carrinho'))
