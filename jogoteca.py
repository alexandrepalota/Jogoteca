from flask import Flask, render_template, request, redirect, session, flash, url_for
import psycopg2

from models import Usuario, Jogo
from dao import JogoDao, UsuarioDao

app = Flask(__name__)
app.secret_key = 'chave_secreta'
app.config['DB_CONNECTION_STRING'] = 'dbname=jogoteca user=postgres password=postgres'

jogo_dao = JogoDao(app.config['DB_CONNECTION_STRING'])
usuario_dao = UsuarioDao(app.config['DB_CONNECTION_STRING'])

@app.route("/")
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route("/novo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route("/criar", methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route("/editar/<id>")
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo)

@app.route("/atualizar", methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    id = request.form['id']
    jogo = Jogo(nome, categoria, console, id=id)
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route("/deletar/<id>")
def deletar(id):
    jogo_dao.deletar(id)
    flash("O jogo foi removido com sucesso")
    return redirect(url_for("index"))

@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route("/autenticar", methods=['POST'])
def autenticar():
    proxima_pagina = request.form['proxima']
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            return redirect(proxima_pagina)
    flash('Não logado, tente novamente')
    return redirect(url_for('login', proxima=proxima_pagina))

@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado')
    return redirect(url_for('index'))

app.run(debug=True)