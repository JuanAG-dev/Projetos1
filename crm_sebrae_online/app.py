from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('crm_sebrae.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota principal (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            return redirect(url_for('clientes'))
        else:
            flash('Usuário ou senha inválidos.')
    return render_template('login.html')

# Rota de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Usuário registrado com sucesso!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Usuário já existe.')
        finally:
            conn.close()
    return render_template('register.html')

# Rota de clientes
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        cpf = request.form['cpf']
        cidade = request.form['cidade']
        celular = request.form['celular']
        email = request.form['email']
        conn = get_db_connection()
        conn.execute('INSERT INTO clientes (nome, sobrenome, cpf, cidade, celular, email) VALUES (?, ?, ?, ?, ?, ?)',
                     (nome, sobrenome, cpf, cidade, celular, email))
        conn.commit()
        conn.close()
        flash('Cliente cadastrado com sucesso!')
    return render_template('clientes.html')

# Rota de projetos
@app.route('/projetos', methods=['GET', 'POST'])
def projetos():
    if request.method == 'POST':
        nome = request.form['nome']
        data = request.form['data']
        local = request.form['local']
        responsaveis = request.form['responsaveis']
        conn = get_db_connection()
        conn.execute('INSERT INTO projetos (nome, data, local, responsaveis) VALUES (?, ?, ?, ?)',
                     (nome, data, local, responsaveis))
        conn.commit()
        conn.close()
        flash('Projeto cadastrado com sucesso!')
    return render_template('projetos.html')

# Rota de agenda
@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        data = request.form['data']
        participantes = request.form['participantes']
        conn = get_db_connection()
        conn.execute('INSERT INTO eventos (tipo, descricao, data, participantes) VALUES (?, ?, ?, ?)',
                     (tipo, descricao, data, participantes))
        conn.commit()
        conn.close()
        flash('Evento adicionado com sucesso!')
    return render_template('agenda.html')

if __name__ == '__main__':
    app.run(debug=True)