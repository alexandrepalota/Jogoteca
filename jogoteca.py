from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = 'chave_secreta'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

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
        return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo='Novo Jogo')

@app.route("/criar", methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')

@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route("/autenticar", methods=['POST'])
def autenticar():
    proxima_pagina = request.form['proxima']
    if 'mestra' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(request.form['usuario'] + ' logou com sucesso!')
        return redirect('/{}'.format(proxima_pagina))
    else:
        flash('Não logado, tente novamente')
        return redirect('/login?proxima={}'.format(proxima_pagina))

@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado')
    return redirect('/')

app.run(debug=True)