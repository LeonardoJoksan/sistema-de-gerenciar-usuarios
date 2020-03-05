from flask import Flask, jsonify, request, render_template
import sqlite3

connection = sqlite3.connect("serralheria_banco.db")
cur = connection.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, login VARCHAR NOT NULL, password VARCHAR NOT NULL)')
cur.close()

app = Flask(__name__)

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

    connection = sqlite3.connect("serralheria_banco.db")
    c = connection.cursor()
    c.execute('SELECT * FROM users WHERE id=?', (id))
    row = c.fetchone()

    return render_template('alterar.html', name=row[1], login=row[2], password=row[3], id=id)

@app.route("/alterar-save", methods=["POST"])
def alterarSave():
    id = request.form["id"]
    name = request.form["name"]
    login = request.form["login"]
    password = request.form["password"]

    connection = sqlite3.connect("serralheria_banco.db")
    c = connection.cursor()

    res = c.execute("UPDATE users SET name=?, login=?, password=? WHERE id=?", (name, login, password, id))
    connection.commit()

    c.execute('SELECT * FROM users WHERE id=?', (id))
    row = c.fetchone()

    return render_template('alterar.html', mensagem="Alterado com sucesso!", name=row[1], login=row[2], password=row[3], id=id)


@app.route("/adicionar-novo", methods=["GET"])
def adicionarNovo():
    return render_template('adicionar_novo.html')

@app.route("/adicionar-novo-save", methods=["POST"])
def adicionarNovoSave():
    name = request.form["name"]
    login = request.form["login"]
    password = request.form["password"]

    connection = sqlite3.connect('serralheria_banco.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, login, password) VALUES (?, ?, ?)", (name, login, password))
    connection.commit()
    cursor.close()
    connection.close()

    return render_template('adicionar_novo.html', mensagem="Adicionado com sucesso!!")

if __name__ == '__main__':
    app.run(debug=True)