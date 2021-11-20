from flask import Flask, render_template

app = Flask(__name__)

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

@app.route("/inicio")
def ola():
    jogo1 = Jogo('God of War', 'Aventura', 'Playstation 4')
    jogo2 = Jogo('Dark Souls 3', 'RPG ação', 'PC')
    jogo3 = Jogo('Sekiro', 'RPG Ação', 'PC')
    jogo4 = Jogo('Forza Horizon 5', 'Corrida', 'Xbox Series X')
    lista = [jogo1, jogo2, jogo3, jogo4]
    return render_template('lista.html', titulo='Jogos', jogos=lista)

app.run()