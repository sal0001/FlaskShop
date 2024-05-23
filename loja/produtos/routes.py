from flask import redirect, render_template, url_for, flash, request, send_from_directory
from flask_login import current_user
from werkzeug.utils import secure_filename
from loja import db, app
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm
import os
from functools import wraps

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
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


def client_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.roleId == 2:
            flash('Ainda não está registado. Por favor registe-se', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def search_products(query):
    search_results = Produto.query.filter(Produto.descricao.ilike(f'%{query}%')).all()
    return search_results

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        search_results = search_products(query)
    else:
        search_results = None
    return render_template('cliente/produto.html', search_results=search_results, categorias=Categoria.query.all(), produtos=Produto.query.all())

@app.route('/categorias')
@login_required
@admin_user
def categorias():
    categorias = Categoria.query.all()
    return render_template('produtos/categorias.html', categorias=categorias)

@app.route('/addcategoria', methods=['GET', 'POST'])
@login_required
@admin_user
def addcategoria():
    form = CategoriaForm()
    if form.validate_on_submit():
        descricao = form.descricao.data
        nova_categoria = Categoria(descricao=descricao)
        db.session.add(nova_categoria)
        db.session.commit()
        flash("Categoria adicionada com successo", 'success')
        return redirect(url_for('addcategoria'))  
    return render_template('/produtos/addcategoria.html', form=form)

@app.route('/removecategoria/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_user
def removecategoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoria removida com successo", 'success')
    return redirect(url_for('categorias'))

@app.route('/updatecategoria/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_user
def updatecategoria(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria.descricao = form.descricao.data
        db.session.commit()
        return redirect(url_for('categorias'))
    elif request.method == 'GET':
        form.descricao.data = categoria.descricao
        flash("Categoria atualizada com successo", 'success')
    return render_template('produtos/updatecategoria.html', form=form, categoria=categoria)

@app.route('/produto')
@client_user
@login_required
def produto():
    produtos = Produto.query.all()
    categorias = Categoria.query.all()
    return render_template('cliente/produto.html', produtos=produtos, categorias=categorias)

@app.route('/filtrar', methods=['POST'])
@client_user
@login_required
def filtrar_produtos():
    categoria_id = request.form.get('categoriaId')  
    if categoria_id:
        produtos = Produto.query.filter_by(categoriaId=categoria_id).all() 
    else:
        produtos = Produto.query.all()
    categorias = Categoria.query.all()
    return render_template('cliente/produto.html', produtos=produtos, categorias=categorias)


@app.route('/addproduto', methods=['GET', 'POST'])
@login_required
@admin_user
def addproduto():
    form = ProdutoForm()
    categorias = Categoria.query.all()
    if form.validate_on_submit():
        descricao = form.descricao.data
        preco = form.preco.data
        categoriaId = form.categoria_id.data
        
        if 'image_url' in request.files:
            image_file = request.files['image_url']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                novo_produto = Produto(descricao=descricao, image_url=filename, preco=preco, categoriaId=categoriaId)
                db.session.add(novo_produto)
                db.session.commit()
                flash("Produto adicionado com sucesso", 'success')  
        return redirect(url_for('addproduto'))
    return render_template('/produtos/addproduto.html', form=form, categorias=categorias)


@app.route('/verprodutos')
@login_required
@admin_user
def produtos():
    produtos = Produto.query.all()
    return render_template('/produtos/produtos.html', produtos=produtos)

@app.route('/updateproduto/<int:id>', methods=['POST'])
@login_required
@admin_user
def updateproduto(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm()
    categorias = Categoria.query.all()
    if form.validate_on_submit():
        descricao = form.descricao.data
        preco = form.preco.data
        categoriaId = form.categoria_id.data
        
        if 'image_url' in request.files:
            image_file = request.files['image_url']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                produto.descricao = descricao
                produto.image_url = filename
                produto.preco = preco
                produto.categoriaId = categoriaId
                db.session.commit()
                flash("Produto atualizado com sucesso", 'success')
        return redirect(url_for('produtos'))
    return render_template('/produtos/updateprodutos.html', form=form, produto=produto, categorias=categorias)

@app.route('/removeproduto/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_user
def removeproduto(id):
    produto = Produto.query.get_or_404(id)
    imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], produto.image_url)

    if os.path.exists(imagem_path):
        os.remove(imagem_path)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto removido com successo", 'success')
    return redirect(url_for('produtos'))