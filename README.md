<h1 align='center'>SWARDEN</h1>

![GitHub License](https://img.shields.io/github/license/LucasGoncSilva/swarden?style=flat&labelColor=%23101010)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LucasGoncSilva/swarden/unittest.yml?style=flat&labelColor=%23101010)  

<h4 align='justify'>Criado em Django como Framework MVC, sWarden funciona como um protótipo real de gerenciador de senhas e credenciais online. Este projeto introduz e apresenta conceitos básicos de segurança de forma prática e descritiva. <br>
Foram utilizadas tanto class-based views quanto function-based views, de modo que os diferentes paradigmas implementados pelo Framework sejam exemplificados de forma prática. <br>
Agrega às medidas de segurança do Django uma lógica inicial do que seria um honeypot, mais de 40 casos de testes incluindo 4 testes de carga para atestar a integridade do sistema e criptografia nos dados armazenados em banco, tudo aplicável em Docker.</h4>

<br>
<hr>

<h2 align='center'>Tecnologias Aplicadas:</h2>

![HTML logo](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS logo](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Sass logo](https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white)
![JavaScript logo](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![Bootstrap logo](https://img.shields.io/badge/Bootstrap-712cf9?style=for-the-badge&logo=bootstrap&logoColor=712cf9&color=fff)

<hr>

![Django logo](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)

<hr>

![PostgreSQL logo](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

<hr>

![Docker logo](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Render logo](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=000&color=fff)
![Supabase Logo](https://img.shields.io/badge/Supabase-181818?style=for-the-badge&logo=supabase&logoColor=3ecf8e)

<br>
<hr>

<h2 align='center'>Features</h2>

- [x] CRUD dos diferentes tipos de segredos armazenados
- [x] Salvar mais de uma conta por serviço (e.g. duas contas do Instagram)
- [x] Exportar dados via e-mail (o mesmo utilizado para acesso ao sistema)
- [ ] Usar Autenticação em Duas Etapas
- [ ] Gerar senhas pseudo-aleatórias como sugestão da plataforma

<br>
<hr>

<h2 align='center'>Arquitetura</h2>


```mermaid
flowchart RL

subgraph CLOUD
    subgraph SYSTEM/APP
        View((View)):::Arch
        Template{Template}:::Arch
        Model{{Model}}:::Arch
    end

    Cover[/"xor(..., encript=True)"/]
    Uncover[/"xor(..., encript=False)"/]

    subgraph DB-INSTANCE
        Database[(Database)]:::Arch
    end
end

User((User))

User -- CreateView:POST ----> View
View --> Model -- insert --> Cover --> Database
Model -- select --> Database
Database --> Uncover --> Model
Model --> View --> Template
Template -- ListView/DetailView --> User

Cover --- Uncover

click Cover "https://github.com/LucasGoncSilva/swarden/blob/main/secret/encript_db.py"
click Uncover "https://github.com/LucasGoncSilva/swarden/blob/main/secret/encript_db.py"

style CLOUD fill:#f0f0ff,color:#4717f6;
style SYSTEM/APP fill:#fff,color:#4717f6;
style DB-INSTANCE fill:#fff,color:#4717f6;
style User fill:#aaf,color:#fff,stroke:#008;
style Cover fill:#afa,color:#070,stroke:#070;
style Uncover fill:#afa,color:#070,stroke:#070;

classDef Arch fill:#f0f0ff,color:#008,stroke:#6f6fff;
```
<h5 align='center'>sWarden's current CRUD architecture</h5>

<br>
<hr>

<h2 align='center'>Starting</h2>

### Buscar/iniciar Migrações (Atualizações) de Banco de Dados

``python3 manager.py makemigrations``

### Atualizar Estrutura do Banco de Dados com Novas Migrações

``python3 manager.py migrate``

### Iniciar Testes Automatizados

``python3 manager.py test``

### Popular Banco de Dados para Execução Local

``python3 manager.py populatedb``

### Iniciar o servidor

``python3 manager.py runserver``

<br>
<hr>

<h2 align='center'>Utilizando</h2>

### Criando uma Conta

Para iniciar, caso não tenha uma conta, crie uma acessando `/conta/registrar` ou seguindo o botão "Regsitrar-se", Preencha e envie o formulário. Feito isso, insira seu `username` e sua `password`, ambos informados no formulário anteriormente. Já possui uma conta? Acesse diretamente por `/conta/entrar` ou siga o botão "Entrar".

<hr>

### Compreendendo a Interface

Após acessar, a todo momento haverá uma barra de navegação no topo das páginas. Você pode utilizá-la para navegar entre os módulos do sistema e realizar algumas ações como:

* Criar e visualizar suas credenciais de login
* Criar e visualizar seus dados de cartões
* Criar e visualizar suas anotações seguras
* Sair do sistema

#### Página Principal

Esta página mostra a quantidade total de cada segredo (credenciais, cartões, anotações) e um breve histórico dos últimos registros feitos. Também permite acessar a página de criação e visualização de cada segredo

#### Página de Criação

Utilizando a barra de navegação (através dos menus dropdown) ou com um botão "Adicionar" na tela inicial você acessa a página de criação. Conforme o formulário é preenchido o campo `slug` - apenas leitura - é autopreenchido com a referência do segredo em questão. Você poderá utilizar esse campo para acessar esse mesmo segredo a partir da URL (e.g. `/segredo/cartao/:slug:`).

Preenchendo e enviando corretamente o formulário você cria um novo segredo com as informações escritas no formulário, sendo posteriormente redirecionado para a página de listagem dos segredos de mesmo tipo (credencial; cartão; anotação).

#### Página de Listagem

Esta página apresenta todos os segredos criados, um tipo por vez. Clickando em um segredo aqui indicado será apresentada uma tela detalhada desse segredo. Não havendo nenhum segredo, haverá uma mensagem indicando a situação com um botão para a tela de criação.

#### Página de Detalhe

Aqui é onde você visualiza os detalhes do segredo escolhido, informação por informação. Junto a isso, há três botões no topo da tela: azul (editar este segredo), vermelho (apagar este segredo) e cinza (adicionar um novo segredo).

<br>
<hr>

<h2 align='center'>To-Do List</h2>

- [ ] Completar a lista de [FEATURES](https://github.com/LucasGoncSilva/swarden#features).
- [ ] Criar as páginas `/sobre` e `/serviços`.
- [ ] Aplicar melhorias de feedback de caracteres nos campos de texto para cada segredo

<br>
<hr>

<h2 align='center'>Avisos</h2>

* This project is already online, but also under development. Use it knowing that some bugs might happen, so keep, at least for now, your secrets that you have another way to access besides sWarden.
* Due to it's gratuity, sWarden supports a limited number of users, requests/online time and secrets stored on it's database. At some point this system will no longer offers registration for new users, preventing the database to colapse.

<br>
<hr>

<h2 align='center'>Licença</h2>

This project is under [MPLv2 - Mozilla Public License Version 2.0](https://choosealicense.com/licenses/mpl-2.0/). Permissions of this weak copyleft license are conditioned on making available source code of licensed files and modifications of those files under the same license (or in certain cases, one of the GNU licenses). Copyright and license notices must be preserved. Contributors provide an express grant of patent rights. However, a larger work using the licensed work may be distributed under different terms and without source code for files added in the larger work.
