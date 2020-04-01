####### INTEGRANTES 
#  1) João Victor (RA: 1800883)         joaoandrade3005@hotmail.com
#  2) Gustavo Cardoso (RA: 1801235)     gcardoso98@gmail.com
#  3) Leonardo Joksan  (RA: 1800618)    leonardojbcordeiro@gmail.com
#  4) Gustavo Zanichelli (RA: 1800167)  tatozanichelli4244@gmail.com

# adhoc, pyOpenSSL (Bibliotecas utilizadas para a utilização do SSL [HTTPS]) 
## Comando utilizado para gerar o certificado " flask run --cert=adhoc "

# Blibiotecas necessárias: Flask, request, jsonify

from flask import Flask, render_template
from flask import jsonify
from flask import request, session
import sqlite3
import os

connection = sqlite3.connect("serralheria_banco.db")
cur = connection.cursor()
# Criar a tabela "users" caso ainda não exista.
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, "
                                                "uid INTEGER DEFAULT 0, "
                                                "email TEXT NOT NULL DEFAULT '@', "
                                                "name TEXT NOT NULL, "
                                                "login TEXT, "
                                                "password TEXT, "
                                                "registerType TEXT DEFAULT 'web', "
                                                "status VARCHAR DEFAULT 0)")
cur.close()

app = Flask(__name__)

if 'SECRET_KEY' in os.environ: app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else: app.config['SECRET_KEY'] = os.urandom(24)

@app.route("/")
def inicio():
    return render_template("login.html", mensagem="Entre no sistema")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", mensagem="Entre no sistema")

@app.route("/entrar", methods=["PUT", "POST"])
def entrar():
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
            session['loginType'] = "web"
            session['login'] = login
            return render_template("login_ok.html", login=login)
        else:
            return render_template("login.html", mensagem="Login/Senha inválido, acesso não permitido.")
        
        c.close()
        connection.close()

@app.route("/entrar-facebook", methods=["PUT", "POST"])
def entrar_facebook():
    uid = request.form["uid"]
    name = request.form["name"]
    email = request.form["email"]

    if uid == "" or name == "" or email == "":
        return "O facebook não retornou as informações de login."
    else:
        connection = sqlite3.connect("serralheria_banco.db")
        c = connection.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND registerType='facebook' AND status='1'", (email,))

        if c.fetchall():
            session['loginType'] = "facebook"
            session['uid'] = uid
            session['name'] = name
            session['email'] = email
            return "loginOK"
        else:
            c.execute('SELECT * FROM users WHERE email=? AND status="0"', (email,))

            if c.fetchall():
                return "Este acesso ainda não foi liberado."
            else:
                c.execute('SELECT * FROM users WHERE email=?', (email,))

                if c.fetchall():
                    return "Este e-mail do facebook já possui cadastro no sistema, favor acessar com Login e Senha."
                else:
                    c.execute("INSERT INTO users (uid, email, name, registerType) VALUES (?, ?, ?, 'facebook')", (uid, email, name))
                    connection.commit()
                    c.close()
                    connection.close()
                    return "Acesso criado, por favor, aguarde para a liberação do seu acesso."

@app.route("/logado", methods=["GET"])
def logado():
    con = sqlite3.connect('serralheria_banco.db')
    db = con.cursor()
    res = db.execute('SELECT * FROM users')
    if session['loginType'] == "facebook":
        return render_template('logado_facebook.html', users=res.fetchall(), uid=session['uid'], email=session['email'], name=session['name'])
    else:
        return render_template('logado.html', users=res.fetchall(), login=session['login'])

@app.route("/excluir", methods=["GET"])
def excluir():
    id = request.args.get('id')

    con = sqlite3.connect('serralheria_banco.db')
    db = con.cursor()
    db.execute("DELETE FROM users WHERE id=?", (id))
    con.commit()

    return render_template('excluir.html', id=id)
    
@app.route("/alterar", methods=["GET"])
def alterar():
    id = request.args.get('id')

    connection = sqlite3.connect("serralheria_banco.db")
    c = connection.cursor()
    c.execute('SELECT * FROM users WHERE id=?', (id))
    row = c.fetchone()

    return render_template('alterar.html', name=row[3], email=row[2], login=row[4], password=row[5], id=id)

@app.route("/alterar-save", methods=["POST"])
def alterarSave():
    id = request.form["id"]
    name = request.form["name"]
    email = request.form["email"]
    login = request.form["login"]
    password = request.form["password"]

    connection = sqlite3.connect("serralheria_banco.db")
    c = connection.cursor()

    c.execute("UPDATE users SET email=?, name=?, login=?, password=? WHERE id=?", (email, name, login, password, id))
    connection.commit()

    c.execute('SELECT * FROM users WHERE id=?', (id))
    row = c.fetchone()

    return render_template('alterar.html', mensagem="Alterado com sucesso!", name=row[3], email=row[2], login=row[4], password=row[5], id=id)


@app.route("/adicionar-novo", methods=["GET"])
def adicionarNovo():
    return render_template('adicionar_novo.html')

@app.route("/adicionar-novo-save", methods=["POST"])
def adicionarNovoSave():
    name = request.form["name"]
    email = request.form["email"]
    login = request.form["login"]
    password = request.form["password"]

    connection = sqlite3.connect('serralheria_banco.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (email, name, login, password) VALUES (?, ?, ?, ?)", (email, name, login, password))
    connection.commit()
    cursor.close()
    connection.close()

    return render_template('adicionar_novo.html', mensagem="Adicionado com sucesso!!")

if __name__ == '__main__':
    #app.run(debug=True)
    app.run('127.0.0.1', debug=True, port=5000, ssl_context='adhoc', use_reloader=False)
    # context = ('local.crt', 'local.key')  #certificate and key files
    # app.run(debug=True, ssl_context=context)
