from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import secrets

# Verificar se o arquivo JSON já existe senão cria um novo
file_path = 'app/database/users.json'
if not os.path.isfile(file_path):
    initial_data = []

    with open(file_path, 'w') as file:
        json.dump(initial_data, file)

# Inicializar o Flask
app = Flask(__name__)


app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'


# Rota para exibir o formulário de registro
@app.route('/')
def index():
    return render_template('index.html')


# Rota para lidar com a requisição de registro
@app.route('/register', methods=['POST'])
def register():
    # Ler os dados do formulário de registro
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    user_type = 'cliente'

    # Verificar se o usuário já existe no arquivo JSON
    with open('app/database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == email:
                return jsonify({'success': False, 'message': 'Email já registrado'})

    # Criar um novo usuário
    new_user = {
        'name': name,
        'email': email,
        'password': password,
        'user_type': user_type
    }

    # Adicionar o novo usuário ao arquivo JSON
    with open('app/database/users.json', 'w') as file:
        users.append(new_user)
        json.dump(users, file)

    return jsonify({'success': True, 'message': 'Registro concluído com sucesso'})


# Rota para lidar com a requisição de login
@app.route('/login', methods=['POST'])
def login():
    # Ler os dados do formulário de login
    email = request.form['email']
    password = request.form['password']

    # Verificar se o usuário existe no arquivo JSON e se a senha está correta
    with open('app/database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == email and user['password'] == password:
                # Usuário encontrado e senha correta
                session['user'] = user
                return redirect(url_for('perfil'))

    # Usuário não encontrado ou senha incorreta
    return jsonify({'success': False, 'message': 'Credenciais inválidas'})


# Rota para lidar com a requisição de login


@app.route('/planos')
def planos():
    return render_template('planos.html')


# Rota para lidar com a requisição de serviços


@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

# Rota para lidar com a requisição de sobre


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para exibir a página de perfil


# Rota para exibir a página de perfil
@app.route('/perfil_index', methods=['GET', 'POST'])
def perfil():
    if 'user' in session:
        user = session['user']
        return render_template('perfil_index.html', user=user)
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(port=5005)
