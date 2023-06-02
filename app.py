from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import datetime
import json
import os
import secrets
from werkzeug.utils import secure_filename


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
                initial_data = {
                    'consultas': []
                }

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
            # Verificar se o animal já possui um plano
            if any(plan['animal'] == animal_name for plan in data['planos']):
                return "Animal já possui um plano"

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

            return True  # Retornar mensagem de sucesso animal adicionado

    return "Animal não encontrado"

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

    # Verificar se o domínio do email é permitido
    if email.endswith('@nutrivet.pt'):
        flash("Contas com esse domínio não podem ser registradas pelo site")
        return redirect(url_for('perfil'))

    # Verificar se o usuário já existe no arquivo JSON
    with open('database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == email:
                flash("Email já existe")
                return redirect(url_for('perfil'))
            if user['name'] == name:
                flash("Nome de usuário já existe")
                return redirect(url_for('perfil'))

    # Verificar a validade da senha
    if len(password) < 1:
        flash("Senha inválida (tamanho mínimo: 1 caractere)")
        return redirect(url_for('perfil'))

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

    flash("Registro concluído com sucesso")
    return redirect(url_for('perfil'))


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
        flash("Tipo de plano inválido")
        return redirect(url_for('index'))

    result = save_plan_to_database(animal_name, plan_type)

    if result == True:
        return redirect(url_for('pagamento'))
    elif result == "Animal já possui um plano":
        flash("Animal já possui um plano")
        return redirect(url_for('perfil_planos'))
    elif result == "Animal não encontrado":
        flash("Animal não encontrado")
        return redirect(url_for('perfil_planos'))
    else:
        flash("Erro inesperado")
        return redirect(url_for('perfil_planos'))


# Rota para lidar com a requisição de login
@app.route('/login', methods=['POST'])
def login():
    # Read the login form data
    email = request.form['email']
    password = request.form['password']

    # Check if the user exists in the JSON file and if the password is correct
    with open('database/users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if user['email'] == email:
                if user['password'] == password:
                    # User found and password is correct
                    session['user'] = user
                    return redirect(url_for('perfil'))
                else:
                    # User found but password is incorrect
                    flash("Senha incorreta")
                    return redirect(url_for('perfil'))

    # User not found
    flash("Email não encontrado")
    return redirect(url_for('perfil'))


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
    if 'user' in session:
        user_type = session['user']['user_type']
        if user_type == 'cliente':
            email = session['user']['email']
            file_path = f'database/{email}.json'

            with open(file_path, 'r') as file:
                data = json.load(file)
                planos = data['planos']

            has_premium_plan = any(
                plan['plan_type'] == 'premium' for plan in planos)
            if has_premium_plan:
                return render_template('urgencia.html')

            # Apenas clientes com plano premium podem entrar em contato de urgência.
            flash(
                "Apenas clientes com plano premium podem entrar em contato de urgência.")
            return redirect(url_for('perfil'))

    # User is not logged in, redirect to login page
    return render_template('login.html')


# Rota para exibir a página de consultas do cliente

@app.route('/perfil_consultas')
def perfil_consultas():
    if 'user' in session:
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            user_data = json.load(file)

        consultas = user_data['consultas']
        animais = user_data['animais']

        # Criar um dicionário com os dias das consultas e a imagem do animal associado
        consultas_dias_imagens = {}
        for consulta in consultas:
            data = datetime.strptime(consulta['data'], '%d/%m/%Y')
            dia = data.day
            animal_nome = consulta['animal']
            imagem = next(
                (animal['imagem'] for animal in animais if animal['name'] == animal_nome), None)

            if dia not in consultas_dias_imagens:
                consultas_dias_imagens[dia] = []

            consultas_dias_imagens[dia].append(imagem)

        return render_template('perfil_consultas.html', consultas_dias_imagens=consultas_dias_imagens)

    return render_template('login.html')


@app.route('/adicionar_animal')
def adicionar_animal():
    return render_template('adicionar_animal.html')


# Rota para exibir a página de perfil de agendamento


@app.route('/perfil_agendar')
def perfil_agendar():
    if 'user' in session:
        user = session['user']
        user_type = user['user_type']
        email = user['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            data = json.load(file)
            animais = data['animais']

        if user_type == 'cliente':
            return render_template('perfil_agendar.html', animais=animais)
        elif user_type == 'veterinario':
            return redirect('/vet_consultas')

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
        flash("Preencha todos os campos")
        return redirect(url_for('perfil_agendar'))
    else:
        if save_consulta_to_database(animal, local, data, hora, descricao):
            flash("Consulta agendada com sucesso")
            return redirect(url_for('perfil'))
        else:
            flash("Erro inesperado")
            return redirect(url_for('perfil'))


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
            return redirect(url_for('vet_index'))

    return render_template('login.html')


# Rota para terminar a sessão do usuário
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


# Rota para mostrar as consultas no vet_index


@app.route('/vet_index')
def vet_index():
    if 'user' in session:
        user_type = session['user']['user_type']
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r') as file:
            user_data = json.load(file)
            consultas = user_data['consultas']

        # Ler os nomes associados aos emails no arquivo users.json
        with open('database/users.json', 'r') as users_file:
            users = json.load(users_file)
            nomes = {user['email']: user['name']
                     for user in users if user['user_type'] == 'cliente'}

        if user_type == 'veterinario':
            return render_template('vet_index.html', consultas=consultas, nomes=nomes)

    return render_template('login.html')


# Rota para mostrar as consultas no vet_consultas


@app.route('/vet_consultas')
def vet_consultas():
    if 'user' in session:
        user_type = session['user']['user_type']
        email = session['user']['email']
        file_path_vet = f'database/{email}.json'

        with open(file_path_vet, 'r') as file_vet:
            vet_data = json.load(file_vet)
            consultas = vet_data.get('consultas', [])

        if user_type == 'veterinario':
            # Criar um dicionário com os dias das consultas e a imagem do animal associado
            consultas_dias_imagens = {}
            for consulta in consultas:
                data = datetime.strptime(consulta['data'], '%d/%m/%Y')
                dia = data.day
                animal_nome = consulta['animal']
                # Obtém o email do dono diretamente da consulta
                owner_email = consulta['email']

                # Abre o arquivo JSON do dono do animal
                file_path_owner = f'database/{owner_email}.json'
                with open(file_path_owner, 'r') as file_owner:
                    owner_data = json.load(file_owner)
                    animais = owner_data.get('animais', [])

                    # Encontra o animal pelo nome
                    animal = next(
                        (animal for animal in animais if animal['name'] == animal_nome), None)

                    if animal:
                        # Obtém a imagem do animal
                        imagem = animal.get('imagem')

                        if dia not in consultas_dias_imagens:
                            consultas_dias_imagens[dia] = []

                        consultas_dias_imagens[dia].append(imagem)

            return render_template('vet_consultas.html', consultas=consultas, consultas_dias_imagens=consultas_dias_imagens)

    return render_template('login.html')


# Rota para mostrar o vet_cliente


@app.route('/vet_cliente', methods=['GET'])
def vet_cliente():
    email_cliente = request.args.get('email_cliente')
    file_path = f'database/{email_cliente}.json'

    try:
        # Buscar o cliente no arquivo JSON do cliente
        with open(file_path, 'r') as file:
            data = json.load(file)
            cliente = data

        # Buscar o nome do cliente no arquivo JSON de usuários
        with open('database/users.json', 'r') as users_file:
            users = json.load(users_file)
            for user in users:
                if user['email'] == email_cliente:
                    nome_cliente = user['name']
                    break
            else:
                nome_cliente = ""

        return render_template('vet_cliente.html', cliente=cliente, nome_cliente=nome_cliente, email_cliente=email_cliente)
    except FileNotFoundError:
        flash("Cliente não encontrado")
        return redirect(url_for('vet_index'))


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

        return render_template('perfil_planos.html', planos=planos, animais=data['animais'])

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


# Rota para lidar com a requisição de remover um animal
@app.route('/remover_animal/<animal_name>')
def remover_animal(animal_name):
    if 'user' in session:
        email = session['user']['email']
        file_path = f'database/{email}.json'

        with open(file_path, 'r+') as file:
            data = json.load(file)

            # Remover o animal da lista de animais do usuário
            animais = data['animais']
            animais = [
                animal for animal in animais if animal['name'] != animal_name]
            data['animais'] = animais

            # Remover o plano associado ao animal, se existir
            planos = data['planos']
            planos = [plano for plano in planos if plano['animal'] != animal_name]
            data['planos'] = planos

            # Salvar as alterações no arquivo JSON
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

        # Remover a imagem do animal
        image_folder = f'static/imagens_animais/'
        image_path = os.path.join(image_folder, f'{email}_{animal_name}.png')
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            flash("Imagem não encontrada")
            return redirect(url_for('perfil_animais'))

        flash("Animal removido com sucesso")
        return redirect(url_for('perfil_animais'))

    return redirect(url_for('login'))

# Rota para lidar com a requisição para adicionar animal form


# Define a pasta de upload e as extensões de arquivo permitidas
UPLOAD_FOLDER = 'database'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


@app.route('/adicionar_animal_form', methods=['POST'])
def adicionar_animal_form():
    # Lê os dados do formulário de adicionar animal: name, idade, raca, genero, peso e imagem
    # Coloca esses dados no arquivo JSON do cliente logado
    # Nesse arquivo, cada pessoa pode ter vários animais e os animais ainda têm uma lista de histórico

    name = request.form['name']
    idade = request.form['idade']
    raca = request.form['raca']
    genero = request.form['genero']
    peso = request.form['peso']
    imagem = request.files['imagem']

    # Verificar se algum campo está vazio
    if not name or not idade or not raca or not genero or not peso:
        flash("Por favor, preencha todos os campos")
        return redirect(url_for('adicionar_animal'))

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
                            flash("Você já tem um animal com esse nome")
                            return redirect(url_for('adicionar_animal'))

                    # Salvar a imagem
                    if imagem and imagem.filename:
                        filename = secure_filename(imagem.filename)
                        extensao = filename.rsplit('.', 1)[1].lower()
                        if extensao not in ['png', 'jpg', 'jpeg', 'webp']:
                            flash(
                                "Formato de imagem inválido. Por favor, escolha uma imagem com formato PNG, JPG, JPEG ou WEBP.")
                            return redirect(url_for('adicionar_animal'))

                        # Renomear a imagem para evitar colisão de nomes
                        imagem_path = f'imagens_animais/{user["email"]}_{name}.{extensao}'
                        # imagem.save(imagem_path) começa por static
                        imagem.save(os.path.join('static', imagem_path))
                    else:
                        # Usar imagem padrão caso nenhuma tenha sido fornecida
                        imagem_path = 'imagens_animais/niko.webp'

                    # Adicionar o novo animal
                    data['animais'].append({
                        'name': name,
                        'idade': idade,
                        'raca': raca,
                        'genero': genero,
                        'peso': peso,
                        'historico': [],
                        'imagem': imagem_path
                    })

                with open(file_path, 'w') as file:
                    json.dump(data, file)

    return redirect(url_for('perfil_animais'))


if __name__ == '__main__':
    app.run(port=5005)
