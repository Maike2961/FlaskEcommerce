from shop import app, db
from flask import render_template, redirect,url_for, flash, request
from shop.models import Item, User
from shop.forms import CadastroForm, LoginForm, ComprarProdutoForm, VenderProdutoForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def home():
    return render_template("home.html") 

@app.route("/produto", methods=["GET", "POST"])
@login_required
def produto():
    compra_form = ComprarProdutoForm()
    venda_form = VenderProdutoForm()
    if request.method == "POST":
        compra_produto = request.form.get('compra_produto')
        produto_obj = Item.query.filter_by(nome=compra_produto).first()
        if produto_obj:
            if current_user.compra_disponivel(produto_obj):
                produto_obj.compra(current_user)
                flash(f"Parabens, vc comprou o produto {produto_obj.nome}", category="success")
            else:
                flash(f"Vc não possui saldo suficiente para comprar o produto {produto_obj.nome}", category="danger")
        
        venda_produto = request.form.get('venda_produto')
        produto_obj_venda = Item.query.filter_by(nome=venda_produto).first()
        if produto_obj_venda:
            if current_user.venda_disponivel(produto_obj_venda):
                produto_obj_venda.venda(current_user)
                flash(f"Parabens, vc vendeu o produto {produto_obj_venda.nome}", category="success")
            else:
                flash(f"Erro na venda do produto {produto_obj_venda.nome}", category="danger")
        return redirect(url_for('produto'))
    if request.method == "GET":
        itens = Item.query.filter_by(dono=None)
        dono_itens = Item.query.filter_by(dono=current_user.id)
    return render_template("produto.html", itens=itens, compra_form=compra_form, dono_itens=dono_itens, venda_form=venda_form)


@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        user = User(
            usuario = form.usuario.data,
            email = form.email.data,
            senhacrip = form.senha1.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('produto'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar: {err}", category='danger')
    return render_template('cadastro.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario_logado = User.query.filter_by(usuario=form.usuario.data).first()
        print(usuario_logado)
        if usuario_logado:
            login_user(usuario_logado)
            flash(f'Seu login é {usuario_logado.usuario}', category='success')
        else:
            flash(f'usuario incorreto {usuario_logado.usuario}', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Voçê fez o logout", category="info")
    return redirect(url_for('home'))