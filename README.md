# ProjetoAS
Projeto Final para a cadeira de Análise de Sistemas da Universidade de Aveiro

Equipa: Henrique Dias (98153), 
        Inês Santos (103477), 
        João Rodrigues (108214), 
        Joaquim Rascão (107484)

Repositório GIT: https://github.com/HDias19/ProjetoAS

Link para o site (hospedado pelos serviços do pythonanywhere): http://nutrivet.pythonanywhere.com/

Logins existentes:
Nome Utilizador: Marco Rodrigues
Email: marco@gmail.com
Palavra-passe: marco1234
Tipo de utilizador: Cliente

Nome Utilizador: João Almeida
Email: joao@gmail.com
Palavra-passe: joao1234
Tipo de utilizador: Cliente

Nome Utilizador: Carlos Silva
Email: carlos@nutrivet.pt
Palavra-passe: carlos1234
Tipo de utilizador: Veterinário

Nome Utilizador: Nelson Costa
Email: nelson@nutrivet.pt
Palavra-passe: nelson1234
Tipo de utilizador: Veterinário


Instruções experimentar a aplicação:

Ponto de vista do visitante:
1. Navegar pelo site:
        - Ao entrar no site, será direcionado para a página inicial. Aqui, encontrará informações gerais sobre os serviços que oferecemos, planos e um pouco sobre quem somos e o que fazemos ao acessar a guia "Sobre".
        - Para obter mais detalhes sobre os serviços, clique na guia "Serviços" no menu superior e o mesmo equivale para a guia "Planos".

2. Registar-se:
        - Para se registar, clique no icon de perfil no canto superior direita do menu. Depois, terá de preencher um formulário com os seus dados pessoais e escolher um nome de utilizador e uma palavra-passe. Após preencher o formulário, clique em "Registar" e caso não haja nenhum erro, será possivel efetuar o login com os dados que acabou de inserir.

        Aspetos a ter cuidado ao registar-se:
        - O nome de utilizador tem de ser único, ou seja, não pode haver dois utilizadores com o mesmo nome de utilizador.
        - O email tem de ser válido, ou seja, tem de conter um "@" e não pode pertencer ao domínio "nutrivet.pt".
        - A palavra-passe tem de ter pelo menos 1 caracterer.

<---------->

Ponto de vista do cliente:
1. Login:
        - Acesse o site e clique no ícone de perfil localizado no canto superior direito do menu.
        - Insira o endereço de email e senha nos campos correspondentes.
        - Clique no botão "Login" e será redirecionado para a página de perfil.

2. Perfil:
        - Ao aceder ao perfil na pagina inicial, poderá ver o seu histórico na clinica.
        - Além disso, você terá acesso às seguintes funcionalidades:
                - Os meus animais: Aqui poderá ver os seus animais de estimação, adicionar novos e remover.
                - Gerir planos: Aqui poderá ver os planos que tem ativos, adicionar novos e remover.
                - Consultas: Aqui poderá ver as consultas que tem marcadas e adicionar novas.
                - Contactar veterinário: Aqui poderá ligar para um veterinário de serviço de urgência, mas apenas se tiver um plano privado ativo.

3. Os meus animais:
        - Aqui consegue ver os seus animais de estimação, adicionar novos e remover.
        - Para adicionar um novo animal, clique no botão "Adicionar animal" e preencha o formulário com os dados do seu animal.
                - É obrigatório preencher todos os campos do formulário, exceto o campo da imagem que caso não seja preenchido, será atribuída uma imagem por defeito.
                - O nome do animal tem de ser único, ou seja, não pode haver dois animais com o mesmo nome para o mesmo utilizador.
        - Para ver os detalhes de um animal, clique no botão "Ver mais" e será redirecionado para a página de detalhes do animal.
                - Nesta página, poderá ver os detalhes do animal, histórico do animal, e remover o animal.
                - Para remover o animal, clique no botão "Remover animal", todos os dados do animal serão apagados assim como quaisquer planos associados ao mesmo e consultas, e será redirecionado para a página "Os meus animais".

4. Gerir planos:
        - Aqui consegue ver os planos que tem ativos, adicionar novos e remover.
        - Para adicionar um novo plano, clique no botão "Aderir a um plano" e preencha o formulário com os dados do plano.
                - É redirecionado para a página de planos onde poderá selecionar um animal e para aderir a um plano, clique no botão "Aderir" do plano que pretende. A seguir é só selecionar o método de pagamento.
        - Para remover um plano, clique no botão "Cancelar plano" e o plano será cancelado e será redirecionado para a página "Gerir planos".

5. Consultas:
        - Aqui consegue ver no calendário a imagem do animal no dia respetivo da consulta que tem marcada.
        - Pode agendar uma consulta clicando no botão "Agendar consulta" e preenchendo o formulário com os dados da consulta.
                - É necessário ter pelo menos um animal para poder agendar uma consulta.
                - É obrigatório preencher todos os campos do formulário.
                - A data da consulta tem de ter o formato "dd/mm/aaaa" e ser um dia válido no mês de junho de 2023.
                - A consulta é atribuída a um veterinário aleatório.

6. Contactar veterinário:
        - Aqui consegue ligar para um veterinário de serviço de urgência, mas apenas se tiver um plano premium ativo.

7. Terminar sessão:
        - Para terminar a sessão, vá a página de perfil e clique no botão "Terminar sessão" e será redirecionado para a página inicial.

<---------->

Ponto de vista do veterinário:
1. Login:
        - Acesse o site e clique no ícone de perfil localizado no canto superior direito do menu.
        - Insira o endereço de email e senha nos campos correspondentes.
        - Clique no botão "Login" e será redirecionado para a página de perfil.

2. Perfil:
        - Ao aceder ao perfil na pagina inicial, poderá ver as suas próximas consultas.
        - Pode também pesquisar por um cliente.
                - Para pesquisar por um cliente, preencha o formulário de "Pesquisar cliente" com o email do cliente e clique no botão "Pesquisar".
                - Caso não saiba o email do cliente, basta escrever qualquer coisa no campo que será mostrada uma lista de todos os clientes, pode inclusive selecionar um cliente da lista.
        - Além disso, você terá acesso no lado esquerdo do perfil à aba consultas.

3. Perfil do cliente:
        - Depois de pesquisar por um cliente é direcionado para o perfil do cliente.
        - Aqui consegue ver os detalhes do cliente, os animais do cliente, planos e as consultas agendadas desse cliente.

4. Consultas:
        - Aqui consegue ver as suas próximas consultas e um calendário com a imagem do animal no dia respetivo da consulta.

5. Terminar sessão:
        - Para terminar a sessão, vá a página de perfil e clique no botão "Terminar sessão" e será redirecionado para a página inicial.