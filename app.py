from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import json
import os
import secrets


# Verificar se o arquivo JSON já existe senão cria um novo
file_path = 'database/users.json'
if not os.path.isfile(file_path):
    initial_data = []
    with open(file_path, 'w') as file:
        json.dump(initial_data, file)

# Verificar se o arquivo JSON para cada usuário já existe senão cria um novo
with open('database/users.json', 'r') as file:
    users = json.load(file)
    for user in users:
        user_type = user['user_type']
        email = user['email']
        file_path = f'database/{email}.json'

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


# Função para obter os animais do usuário


def get_user_animals():
    if 'user' in session:
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['animais']
    return []


# Função para salvar o plano na base de dados
def save_plan_to_database(animal_name, plan_type):
    user = session['user']
    email = user['email']
    file_path = f'database/{email}.json'

    with open(file_path, 'r+') as file:
        data = json.load(file)

        animal = next(
            (animal for animal in data['animais'] if animal['name'] == animal_name), None)
        if animal:
            # Obter a data atual em formato dia/mês/ano
            adhesion_date = datetime.now().strftime('%d/%m/%Y')
            data['planos'].append({
                'animal': animal_name,
                'plan_type': plan_type,
                'data': adhesion_date
            })

            file.seek(0)  # Mover o cursor para o início do arquivo
            json.dump(data, file, indent=4)
            file.truncate()  # Reduzir o tamanho do arquivo, se necessário

            return True

    return False

# Função para salvar a consulta na base de dados


def save_consulta_to_database(animal, local, data_consulta, hora, descricao):
    if 'user' in session:
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r+') as file:
            user_data = json.load(file)

            consultas = user_data['consultas']
            consultas.append({
                'animal': animal,
                'local': local,
                'data': data_consulta,
                'hora': hora,
                'descricao': descricao
            })

            file.seek(0)
            json.dump(user_data, file, indent=4)
            file.truncate()

        return True

    return False


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
    with open('database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == email:
                return render_template('popup.html', message='BAD: Email já registrado')

    # Criar um novo usuário
    new_user = {
        'name': name,
        'email': email,
        'password': password,
        'user_type': user_type
    }

    # Adicionar o novo usuário ao arquivo JSON
    with open('database/users.json', 'w') as file:
        users.append(new_user)
        json.dump(users, file)

    # Cria o arquivo JSON com o email do cliente
    file_path = f'database/{email}.json'
    initial_data = {
        'animais': [],
        'planos': [],
        'consultas': []
    }
    with open(file_path, 'w') as file:
        json.dump(initial_data, file)

    return render_template('popup.html', message='GOOD: Registro concluído com sucesso')

# Rota para lidar com a requisição de mostrar os animais do usuário na pagina de planos


@app.route('/planos')
def planos():
    if 'user' in session:
        user_type = session['user']['user_type']
        if user_type == 'cliente':
            user_animals = get_user_animals()
            return render_template('planos.html', user_animals=user_animals)
    return redirect(url_for('planos_basica'))


# Rota para lidar com a requisição de adicionar um plano na base de dados


@app.route('/adicionar_plano', methods=['POST'])
def adicionar_plano():
    plan_type = request.form.get('plan_type')

    if plan_type == 'standard':
        # Obtenha o campo com o sufixo "_standard"
        animal_name = request.form.get('animal_standard')
    elif plan_type == 'premium':
        # Obtenha o campo com o sufixo "_premium"
        animal_name = request.form.get('animal_premium')
    else:
        return render_template('popup.html', message='BAD: Tipo de plano inválido')

    save_plan_to_database(animal_name, plan_type)

    return redirect(url_for('perfil_planos'))


# Rota para lidar com a requisição de login
@app.route('/login', methods=['POST'])
def login():
    # Ler os dados do formulário de login
    email = request.form['email']
    password = request.form['password']

    # Verificar se o usuário existe no arquivo JSON e se a senha está correta
    with open('database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == email and user['password'] == password:
                # Usuário encontrado e senha correta
                session['user'] = user
                return redirect(url_for('perfil'))

    # Usuário não encontrado ou senha incorreta
    return render_template('popup.html', message='BAD: Credenciais inválidas')


# Rotas para páginas estáticas
@app.route('/servicos')
def servicos():
    return render_template('servicos.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/pagamento')
def pagamento():
    return render_template('pagamento.html')


@app.route('/planos_basica')
def planos_basica():
    return render_template('planos_basica.html')


@app.route('/contactar')
def contactar():
    return render_template('urgencia.html')


@app.route('/perfil_consultas')
def perfil_consultas():
    return render_template('perfil_consultas.html')


@app.route('/vet_consultas')
def vet_consultas():
    return render_template('vet_consultas.html')


@app.route('/adicionar_animal')
def adicionar_animal():
    return render_template('adicionar_animal.html')


# Rota para exibir a página de perfil de agendamento


@app.route('/perfil_agendar')
def perfil_agendar():
    if 'user' in session:
        user = session['user']
        email = user['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            data = json.load(file)
            animais = data['animais']

        return render_template('perfil_agendar.html', animais=animais)

    return render_template('login.html')


# Rota para agendar consulta


@app.route('/agendar', methods=['POST'])
def agendar():
    animal = request.form.get('animal')
    local = request.form.get('local')
    data = request.form.get('data')
    hora = request.form.get('hora')
    descricao = request.form.get('descricao')
    # Verificar se nenhum campo está vazio
    if not animal or not local or not data or not hora or not descricao:
        return render_template('popup.html', message='BAD: Preencha todos os campos')
    else:
        if save_consulta_to_database(animal, local, data, hora, descricao):
            return render_template('popup.html', message='GOOD: Consulta agendada com sucesso')
        else:
            return render_template('popup.html', message='BAD: Usuário não logado')


# Rota para a ficha do animal


@app.route('/animal/<nome_animal>')
def animal(nome_animal):
    if 'user' in session:
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            user_data = json.load(file)
            animais = user_data['animais']
            consultas = user_data['consultas']

            animal = next(
                (animal for animal in animais if animal['name'] == nome_animal), None)

        if animal:
            consultas_animal = [
                consulta for consulta in consultas if consulta['animal'] == nome_animal
            ]
            return render_template('animal.html', animal=animal, consultas=consultas_animal)

    return redirect(url_for('login'))


# Rota para exibir a página de perfil


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user' in session:
        user_type = session['user']['user_type']
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            user_data = json.load(file)
            consultas = user_data['consultas']

        if user_type == 'cliente':
            return render_template('perfil_index.html', consultas=consultas)
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
    if 'user' in session:
        user = session['user']
        email = user['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            data = json.load(file)
            animais = data['animais']

        return render_template('perfil_animais.html', animais=animais)

    return render_template('login.html')


# Rota para lidar com a requisição de os meus planos
@app.route('/perfil_planos')
def perfil_planos():
    if 'user' in session:
        user = session['user']
        email = user['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            data = json.load(file)
            planos = data['planos']

        return render_template('perfil_planos.html', planos=planos)

    return render_template('login.html')

# Rota para lidar com a requisição de cancelar um plano


@app.route('/cancelar_plano/<animal>/<plan_type>')
def cancelar_plano(animal, plan_type):
    if 'user' in session:
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r+') as file:
            data = json.load(file)

            animal_plans = data['planos']
            for plan in animal_plans:
                if plan['animal'] == animal and plan['plan_type'] == plan_type:
                    animal_plans.remove(plan)
                    break

            file.seek(0)  # Mover o cursor para o início do arquivo
            json.dump(data, file, indent=4)
            file.truncate()  # Reduzir o tamanho do arquivo, se necessário

            return redirect(url_for('perfil_planos'))

    return redirect(url_for('login'))


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
    with open('database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == session['user']['email']:
                file_path = f'database/{user["email"]}.json'
                with open(file_path, 'r') as file:
                    data = json.load(file)

                    # Verificar se o animal já existe
                    for animal in data['animais']:
                        if animal['name'] == name:
                            return render_template('popup.html', message='BAD: Você já tem um animal com esse nome')

                    # Adicionar o novo animal
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

    return redirect(url_for('perfil_animais'))


if __name__ == '__main__':
    app.run(port=5005)
