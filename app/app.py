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

# Verificar se o arquivo JSON para cada usuário já existe senão cria um novo
with open('app/database/users.json', 'r') as file:
    users = json.load(file)
    for user in users:
        user_type = user['user_type']
        email = user['email']
        file_path = f'app/database/{email}.json'

        if not os.path.isfile(file_path):
            initial_data = {
                'animais': [],
                'planos': [],
                'consultas': []
            }

            if user_type == 'veterinario':
                initial_data['consultas'] = []

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

    # Cria o arquivo JSON com o email do cliente
    file_path = f'app/database/{email}.json'
    initial_data = {
        'animais': [],
        'planos': [],
        'consultas': []
    }
    with open(file_path, 'w') as file:
        json.dump(initial_data, file)

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


# Rotas para páginas estáticas
@app.route('/planos')
def planos():
    return render_template('planos.html')


@app.route('/servicos')
def servicos():
    return render_template('servicos.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/contactar')
def contactar():
    return render_template('urgencia.html')


# Rota para exibir a página de perfil
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user' in session:
        user_type = session['user']['user_type']
        if user_type == 'cliente':
            return render_template('perfil_index.html')
        elif user_type == 'veterinario':
            return render_template('vet_index.html')
    return render_template('login.html')


# Rota para terminar a sessão do usuário
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


# Rota para lidar com a requisição de os meus animais
@app.route('/perfil_animais')
def perfil_animais():
    return render_template('perfil_animais.html')


# Rota para lidar com a requisição de os meus planos
@app.route('/perfil_planos')
def perfil_planos():
    return render_template('perfil_planos.html')


# Rota para lidar com a requisição de as minhas consultas
@app.route('/perfil_consultas')
def perfil_consultas():
    return render_template('perfil_consultas.html')


# Rota para lidar com a requisição das consultas do veterinário
@app.route('/vet_consultas')
def vet_consultas():
    return render_template('vet_consultas.html')


# Rota para lidar com a requisição para adicionar animal
@app.route('/adicionar_animal')
def adicionar_animal():
    return render_template('adicionar_animal.html')


# Rota para lidar com a requisição para adicionar animal form
@app.route('/adicionar_animal_form', methods=['POST'])
def adicionar_animal_form():
    # Lê os dados do formulário de adicionar animal: name, idade, raca, genero e peso
    # Coloca esses dados no arquivo JSON do cliente logado
    # Nesse arquivo, cada pessoa pode ter vários animais e os animais ainda têm uma lista de histórico

    name = request.form['name']
    idade = request.form['idade']
    raca = request.form['raca']
    genero = request.form['genero']
    peso = request.form['peso']

    # Verificar se o usuário já existe no arquivo JSON
    with open('app/database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == session['user']['email']:
                file_path = f'app/database/{user["email"]}.json'
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    data['animais'].append({
                        'name': name,
                        'idade': idade,
                        'raca': raca,
                        'genero': genero,
                        'peso': peso,
                        'historico': []
                    })
                with open(file_path, 'w') as file:
                    json.dump(data, file)

    return render_template('perfil_animais.html')


@app.route('/cancelar_plano')
def cancelar_plano():
    return render_template('planos.html')


if __name__ == '__main__':
    app.run(port=5005)
