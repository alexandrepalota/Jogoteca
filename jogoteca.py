from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'chave_secreta'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('alexandre', 'Alexandre Palota', '123')
usuario2 = Usuario('fulano', 'Fulano de Tal', '456')
usuario3 = Usuario('beltrano', 'Beltrano de Tal', '789')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2, usuario3.id: usuario3}

jogo1 = Jogo('God of War', 'Aventura', 'Playstation 4')
jogo2 = Jogo('Dark Souls 3', 'RPG ação', 'PC')
jogo3 = Jogo('Sekiro', 'RPG Ação', 'PC')
jogo4 = Jogo('Forza Horizon 5', 'Corrida', 'Xbox Series X')
lista = [jogo1, jogo2, jogo3, jogo4]

@app.route("/")
def index():
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
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route("/autenticar", methods=['POST'])
def autenticar():
    proxima_pagina = request.form['proxima']

    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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