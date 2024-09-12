<h1 align="center">
  <img src="./logo.svg" height="300" width="300" alt="Logo SWARDEN" /><br>
  SWARDEN
</h1>

![GitHub License](https://img.shields.io/github/license/LucasGoncSilva/swarden?labelColor=101010)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LucasGoncSilva/swarden/django_unittest.yml?style=flat&labelColor=%23101010)

Criado em Django como Framework MVC, sWarden funciona como um protótipo real de gerenciador de senhas e credenciais online. Este projeto introduz e apresenta conceitos básicos de segurança de forma prática e descritiva.

Foram utilizadas tanto class-based views quanto function-based views, de modo que os diferentes paradigmas implementados pelo Framework sejam exemplificados de forma prática.

Agrega às medidas de segurança do Django uma lógica inicial do que seria um honeypot, mais de 140 casos de testes incluindo 4 testes de carga para atestar a integridade do sistema e criptografia nos dados armazenados em banco, tudo aplicável em Docker.

## Stack

![HTML logo](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS logo](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Sass logo](https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white)
![JavaScript logo](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![Bootstrap logo](https://img.shields.io/badge/Bootstrap-712cf9?style=for-the-badge&logo=bootstrap&logoColor=712cf9&color=fff)

![Django logo](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)

![PostgreSQL logo](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

![Docker logo](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Render logo](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=000&color=fff)
![Supabase Logo](https://img.shields.io/badge/Supabase-181818?style=for-the-badge&logo=supabase&logoColor=3ecf8e)

## Arquitetura

A arquitetura pode ser detalhada de forma geral em dois níveis: web e database. As mecânicas são abstraídas a um nível geral, evitando detalhes profundos que confundam à agregar, apresentando uma visão comportamental em escala "macro" seguindo o fluxo de dados sem focar no "micro", como cada ação de cada função. Acompanhe abaixo o fluxo de informações na Web, seguido da estruturação e arquitetura o Banco de Dados (Para mais detalhes sobre o Banco de Dados acesse [https://dbdocs.io/lucasgoncsilva04/SWARDEN](https://dbdocs.io/lucasgoncsilva04/SWARDEN)):

### Web

<!-- ![Arquitetura de Funcionamento do Projeto](./web/arch.svg) -->

```mermaid
flowchart LR


User((User))

subgraph CLOUD
    subgraph RENDER
        LB(Load Balancer):::Arch
        Dispatcher[Req. Dispatcher]:::Arch
        Template{{Template}}:::Arch
        View{View}:::Arch
        Model{{Model}}:::Arch
    end

    subgraph SUPABASE
        Database[(Database)]
    end
end


Template ~~~ Model

User --> LB --> Dispatcher --> View --> Model

Model -->|Insert / Update| Database
Model -->|Select| Database

Database --> Model --> View --> Template --> Dispatcher --> LB --> User


style CLOUD fill:#1117,color:#44b78b,stroke:#ccc;
style RENDER fill:#1117,color:#44b78b,stroke:#ccc;
style SUPABASE fill:#1117,color:#44b78b,stroke:#ccc;
style User fill:#fff,color:#0c4b33,stroke:#0c4b33;
style Database fill:#dfd,color:#0c4b33,stroke:#0c4b33;

classDef Arch fill:#0c4b33,color:#efe,stroke:#efe;

linkStyle 1,2,3,4,5,6 stroke:#0f0,color:#efe
linkStyle 7,8,9,10,11,12 stroke:#fff,color:#efe
```

### DB

![Arquitetura do Banco de Dados](./db/db_schema.svg)

## Básico

Antes de iniciar com o desenvolvimento e os comandos, é importante definir as variáveis de ambiente no seu ambiente de desenvolvimento. Abaixo a listagem de quais definir:

| Variável                 | Caráter                | Responsabilidade                                                                    |
| :----------------------- | :--------------------- | :---------------------------------------------------------------------------------- |
| `DJANGO_SETTINGS_MODULE` | `str - optional`       | Definir o módulo de configurações a ser utilizado.<br>Default `CORE.settings.dev`   |
| `CAPTCHA_TEST_MODE`      | `bool - optional`      | Permitir o bypass do captcha nas telas de acesso.<br>Default `True`                 |
| `DATABASE_NAME`          | `str - optional`       | Definir o nome de acesso do Banco de Dados.<br>Default `postgres`                   |
| `DATABASE_USER`          | `str - optional`       | Definir o usuário de acesso do Banco de Dados.<br>Default `postgres`                |
| `DATABASE_PASSWORD`      | `str - optional`       | Definir a senha de acesso do Banco de Dados.<br>Default `postgres`                  |
| `DATABASE_HOST`          | `str - optional`       | Definir o host de acesso do Banco de Dados.<br>Default `localhost`                  |
| `DEBUG`                  | `bool - optional`      | Definir traceback e informações de debug em páginas browser.<br>Default `True`      |
| `SECRET_KEY`             | `str - optional`       | Definir chave de criptografia e segurança do projeto.<br>Default `cw%t5...ba^m3)`   |
| `ALLOWED_HOSTS`          | `list[str] - optional` | Definir lista de endereços URL válidos para execução do projeto.<br>Default `['*']` |

### Buscar/iniciar Migrações (Atualizações) de Banco de Dados

`python3 manager.py makemigrations`

### Atualizar Estrutura do Banco de Dados com Novas Migrações

`python3 manager.py migrate`

### Iniciar Testes Automatizados

`python3 manager.py test [--parallel N]`

### Iniciar Testes Automatizados c/ Cobertura

`python3 manager.py testwithcoverage`

### Popular Banco de Dados para Execução Local

`python3 manager.py populateuser` para usuários

`python3 manager.py populatesecret` para segredos - após executar o comando anterior

### Iniciar o Servidor

`python3 manager.py runserver`

## Utilizando

### Criando uma Conta

Para iniciar, caso não tenha uma conta, crie uma acessando `/conta/registrar` ou seguindo o botão "Regsitrar-se", Preencha e envie o formulário. Feito isso, insira seu `username` e sua `password`, ambos informados no formulário anteriormente. Já possui uma conta? Acesse diretamente por `/conta/entrar` ou siga o botão "Entrar".

<hr>

### Compreendendo a Interface

Após acessar, a todo momento haverá uma barra de navegação no topo das páginas. Você pode utilizá-la para navegar entre os módulos do sistema e realizar algumas ações como:

- Criar e visualizar suas credenciais de login
- Criar e visualizar seus dados de cartões
- Criar e visualizar suas anotações seguras
- Sair do sistema

#### Página Principal

Esta página mostra a quantidade total de cada segredo (credenciais, cartões, anotações) e um breve histórico dos últimos registros feitos. Também permite acessar a página de criação e visualização de cada segredo

#### Página de Criação

Utilizando a barra de navegação (através dos menus dropdown) ou com um botão "Adicionar" na tela inicial você acessa a página de criação. Conforme o formulário é preenchido o campo `slug` - apenas leitura - é autopreenchido com a referência do segredo em questão. Você poderá utilizar esse campo para acessar esse mesmo segredo a partir da URL (e.g. `/segredo/cartao/:slug:`).

Preenchendo e enviando corretamente o formulário você cria um novo segredo com as informações escritas no formulário, sendo posteriormente redirecionado para a página de listagem dos segredos de mesmo tipo (credencial; cartão; anotação).

#### Página de Listagem

Esta página apresenta todos os segredos criados, um tipo por vez. Clickando em um segredo aqui indicado será apresentada uma tela detalhada desse segredo. Não havendo nenhum segredo, haverá uma mensagem indicando a situação com um botão para a tela de criação.

#### Página de Detalhe

Aqui é onde você visualiza os detalhes do segredo escolhido, informação por informação. Junto a isso, há três botões no topo da tela: azul (editar este segredo), vermelho (apagar este segredo) e cinza (adicionar um novo segredo).

## To-Do List

- [ ] Usar Autenticação em Duas Etapas
- [ ] Gerar senhas pseudo-aleatórias como sugestão da plataforma
- [ ] Criar as páginas `/sobre` e `/serviços`.
- [ ] Aplicar melhorias de feedback de caracteres nos campos de texto para cada segredo

## Contrib

### Escrevendo Testes de Models

```py
class MyModelTestCase(TestCase):
    def setUp(self) -> None:
        self.model1: MyModel = MyModel.objects.create(...)

        self.model2: MyModel = MyModel.objects.create(...)

        self.model3: MyModel = MyModel.objects.create(...)

        self.model4: MyModel = MyModel.objects.create(...)

        self.model5: MyModel = MyModel.objects.create(...)

    def test_model_instance_validity(self) -> None:
        """Tests model instance of correct class"""

        for model in MyModel.objects.all():
            with self.subTest(model=model):
                self.assertIsInstance(model, MyModel)

    def test_model_special_str_method_return(self) -> None:
        """Tests model return value of __str__ method"""

        model = MyModel.objects.get(pk=self.model.pk)

        self.assertEqual(model.__str__(), ...)

    def test_model_key_value_assertion(self) -> None:
        """Tests model correct attribuition of value"""

        model1: MyModel = MyModel.objects.get(pk=self.model1.pk)

        self.assert...(...)
        ...

    def test_model_create_validity(self) -> None:
        """Tests model creation integrity and validation"""

        model1: MyModel = MyModel.objects.get(pk=self.model1.pk)
        model2: MyModel = MyModel.objects.get(pk=self.model2.pk)
        model3: MyModel = MyModel.objects.get(pk=self.model3.pk)
        model4: MyModel = MyModel.objects.get(pk=self.model4.pk)
        model5: MyModel = MyModel.objects.get(pk=self.model5.pk)

        self.assertEqual(MyModel.objects.all().count(), 5)

        self.assertTrue(model1.is_valid())
        self.assertTrue(model2.is_valid())
        self.assertTrue(model3.is_valid())
        self.assertFalse(model4.is_valid())
        self.assertFalse(model5.is_valid())

    def test_model_update_validity(self) -> None:
        """Tests model update integrity and validation"""

        MyModel.objects.filter(pk=self.model4.pk).update(...)

        MyModel.objects.filter(pk=self.model5.pk).update(...)

        for model in MyModel.objects.all():
            with self.subTest(model=model):
                self.assertTrue(model.is_valid())

    def test_model_delete_validity(self) -> None:
        """Tests model correct deletion"""

        for model in MyModel.objects.all():
            if not model.is_valid():
                model.delete()

        self.assertEqual(MyModel.objects.all().count(), <int>)

    def test_model_db_exception_raises(self) -> None:
        """Tests model correct integrity and validation with raised exceptions"""

        # Expecting raises
        params: list[dict[str, MyModel | str]] = [
            {'field': 'value'},
            {'field': 'value'},
            {'field': 'value'},
            {'field': 'value'},
            {'field': 'value'},
            {'field': 'value'},
            {'field': 'value'},
            {'field': 'value'},
            {'field': 'value'},
        ]

        for case, scenario in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: MyModel = MyModel(**scenario)
                        instance.full_clean()

        raise_kwargs: dict[str, dict[str, ...]] = {
            'model1': {...},
            'model2': {...},
            ...
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(Exception):
                    with atomic():
                        instance: MyModel = MyModel(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, ...]] = {
            'model1': {...},
            'model2': {...},
            ...
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: MyModel = MyModel(**no_raise_kwargs[scenario])
                instance.full_clean()
```

### Escrevendo Testes de Views

```py
class BaseExampleTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            password='password',
            email='user@email.com',
        )

        self.CONSTANT: ... = ...
        self.CONSTANT: ... = ...


class Example[Create|List|Detail|Update|Delete]ViewTestCase(BaseExampleTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /example/view | anonymous user"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse(ENDPOINT))

        self.assertEqual(res.status_code, xxx)
        self.assertRedirects(res, reverse(ENDPOINT))

        res: HttpResponse = self.client.get(
            reverse(ENDPOINT), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, TEMPLATE)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /example/view | authenticated user"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse(ENDPOINT))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, TEMPLATE)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user(self) -> None:
        """POST /example/view | anonymous user"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(reverse(ENDPOINT), {DATA: HERE})

        self.assertEqual(res.status_code, xxx)
        self.assertRedirects(res, reverse(ENDPOINT))

        res: HttpResponse = self.client.post(
            reverse(ENDPOINT),
            {DATA: HERE},
            follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, TEMPLATE)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user(self) -> None:
        """POST /example/view | authenticated user"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(reverse(ENDPOINT))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, TEMPLATE)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
```

## Licença

This project is under [MPLv2 - Mozilla Public License Version 2.0](https://choosealicense.com/licenses/mpl-2.0/). Permissions of this weak copyleft license are conditioned on making available source code of licensed files and modifications of those files under the same license (or in certain cases, one of the GNU licenses). Copyright and license notices must be preserved. Contributors provide an express grant of patent rights. However, a larger work using the licensed work may be distributed under different terms and without source code for files added in the larger work.
