from flask import Flask, jsonify, request, render_template
from alunos_api import alunos_app, alunos_db
from professores_api import professores_app, professores_db
import sqlite3

connection = sqlite3.connect("serralheria_banco.db")
cur = connection.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, login VARCHAR NOT NULL, password VARCHAR NOT NULL)')
cur.close()

app = Flask(__name__)
app.register_blueprint(alunos_app)
app.register_blueprint(professores_app)

def inserir_usuario(name, login, password):
    connection = sqlite3.connect('serralheria_banco.db')
    cursor = connection.cursor()
    sql = "INSERT INTO users (name, login, password) VALUES (?, ?, ?)"
    cursor.execute(sql, (name, login, password))
    id_cliente = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return id_cliente

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", mensagem="Entre no sistema")

@app.route("/form_teste", methods=["PUT", "POST"])
def form_teste():
    login = request.form["login"]
    senha = request.form["password"]

    if login == "":
        return render_template("login.html", mensagem="Voce deve digitar um Login.")
    elif senha == "":
        return render_template("login.html", mensagem="Voce deve digitar uma senha.")
    else:
        connection = sqlite3.connect("serralheria_banco.db")
        c = connection.cursor()
        c.execute('SELECT * FROM users WHERE login=? AND password=?', (login, senha))

        if c.fetchall():
            return render_template("login_ok.html", login=login)
        else:
            return render_template("login.html", mensagem="Login invalido.")
        
        c.close()
        connection.close()

@app.route("/logado", methods=["GET"])
def logado():
    con = sqlite3.connect('serralheria_banco.db')
    db = con.cursor()
    res = db.execute('SELECT * FROM users')
    return render_template('logado.html', users=res.fetchall())

@app.route("/excluir", methods=["GET"])
def excluir():
    id = request.args.get('id')

    con = sqlite3.connect('serralheria_banco.db')
    db = con.cursor()
    res = db.execute("DELETE FROM users WHERE id=?", (id))
    con.commit()

    return render_template('excluir.html', id=id)
    
@app.route("/alterar", methods=["GET"])
def alterar():
    id = request.args.get('id')
    save = request.args.get('save')

    if save == "sim":
        
        return render_template('alterar.html', mensagem="Alterado com sucesso!", id=id)
    else:
        return render_template('alterar.html', id=id)

if __name__ == '__main__':
    app.run(debug=True)