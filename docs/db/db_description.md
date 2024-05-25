# sWarden: Arquitetura do Banco de Dados

Criado em Django como Framework MVC, sWarden funciona como um protótipo real de gerenciador de senhas e credenciais online. Este projeto integerroduz e apresenta conceitos básicos de segurança de forma prática e descritiva.

Foram utilizadas tanto class-based views quanto function-based views, de modo que os diferentes paradigmas implementados pelo Framework sejam exemplificados de forma prática.

Agrega às medidas de segurança do Django uma lógica inicial do que seria um honeypot, mais de 140 casos de testes incluindo 4 testes de carga para atestar a integeregridade do sistema e criptografia nos dados armazenados em banco, tudo aplicável em Docker.

O Banco de Dados possui uma importância monumental, pois é nele onde se concentram as informações mais sensíveis de TODO o projeto. Sua arquitetura impacta diretamente todos os pontos onda há contato com ele, por menor que seja.

O desenho de cada tabela, as relações de chaves estrangeiras e até os tipos de dados escolhidos para cada coluna influenciam a performance de tudo, partindo do próprio Banco e indo ao Front-end passando pelo Back-end.

Nesta documentação serão apresentados a engine escolhida, a arquitetura e estrutura do Banco de Dados, cada uma de suas tabelas aqui existentes, os tipos de dados das colunas, as referências de chaves estrangeias e quaisquer outras mecânicas que possuam a devida importância para estarem documentadas.

---

## PostgreSQL

"O Mais Avançado Banco de Dados do Mundo", como ele mesmo define, é um sistema de gerenciamento de banco de dados relacional e objeto-relacional de código aberto. Ele é amplamente utilizado por sua robustez, extensibilidade e conformidade com os padrões SQL.

Definitivamente não é o mais veloz, bancos de dados não-relacionais como Redis ocupam esse lugar, também não é o mais compacto, SQLite é o comercialmente mais compacto, mas ele é o mais eficiente em equilibrar todos os elementos. Ser muito rápido, extremamente confiável, facilmente trabalhado, globalmente disponibilizado, avançado quanto às transações ACID, personalizável e ainda possuir uma comunidade extremamente ativa - também por ser de código aberto - o torna líder de mercado, escolha quase que padrão para a maioria dos projetos.

Os elementos descritos acima contribuem diretamente para a escolha da engine e do Banco de Dados Postgres, atentendo às demandas deste projeto de maneira consistente ~~e gratuita~~.

## Tabelas

O Banco de Dados do sWarden é arquitetado com duas frentes conectadas: usuários e segredos. A primeira frente não possui mistério algum; a segunda frente se responsabiliza dos segredos referentes a cada usuário; ambos descritos abaixo:

### Usuários

* `User`: Controle de usuários cadastrados, ativos e inativos, comuns e administradores
* `ActivationAccountTokenUser`: Tokens de ativação de novos usuários, recém-cadastrados, ainda não plenamente aptos

### Segredos

* `LoginCredential`: Credenciais de acessos para serviços como Gmail, Amazon Prime, GitHub, ...
* `Card`: Cartões de débido, crédito, ...
* `SecurityNote`: Notas e anotações de seguranças

## Tipos de Dados

Apesar da arquitetura possuir 5 tabelas principais (demais tabelas com responsabilidades administrativas do próprio Framework Django) com mais de 43 colunas somadas, os tipos de dados utilizados nas tabelas se resumem à apenas 5 tipos: `bool`, `date`, `uuid`, `integer`, `timestamp` e `varchar`.

`bool`: 1 byte de tamanho, determina um valor binário como positivo/negativo, on/off, 0/1
`date`: 4 bytes de tamanho, determina uma data entre 4713 AC e 5874897 DC com precisão de 1 dia
`integer`: 8 bytes de tamanho, determina um integereiro entre -2.147.483.648 to +2.147.483.647 (2bi)
`timestamp`: 8 bytes de tamanho, determina data e hora entre 4713 AC e 5874897 DC com precisão de 1 microsegundo
`uuid`: 16 bytes de tamanho, utilizado para determinar IDs não-incrementais integereiros, gerados por um algoritmo, neste caso o v4
`varchar`: tamanho em bytes variado, define sequências de caracteres, strings, variando o tamanho em bytes com especificação + 1 (e.g. varchar(10) -> 11 bytes)

A escolha de tipos de dados é estratégica para o balanceamento entre espaço de armazenamento e velocidade de acesso, onde inteiros e UUIDs são utilizados para identificar registros de forma eficiente e segura, varchar com limitação de tamanho em campos de texto (first_name, last_name, email, etc.) para economizar espaço (delimitando-o) e melhorar a performance e, por fim, timestamps se encarregando da facilitação de operações temporais, como ordenação e filtro por data de criação ou atualização.

## Referências - Chaves Estrangeiras

Chaves estrangeiras são referências de uma tabela a outra, garantindo a integridade referencial entre elas. Elas estabelecem um vínculo entre a coluna de uma tabela, chamada de chave estrangeira, e a coluna primária da tabela referenciada.

No PostgreSQL, ao definir uma chave estrangeira, asseguramos que os valores dessa coluna correspondam a valores existentes na coluna primária referenciada, impedindo dados órfãos e mantendo a consistência dos relacionamentos no Banco de Dados. Os relacionamentos entre as tabelas do Banco de Dados se faz com odeterminado a seguir:

`ActivationAccountToken.user` many-to-one `User.ID`
`LoginCredential.owner` many-to-one `User.ID`
`Card.owner` many-to-one `User.ID`
`SecurityNote.owner` many-to-one `User.ID`

Onde cada Token de Ativação, Credencial de Login, Cartão e Anotação de Segurança só pode estar conectado a um único Usuário, porém, cada Usuário pode se conectar e possuir um ou mais dos demais itens.

## Normalização e Desnormalização

Normalização é o processo de organização de dados em um banco de dados. Isso inclui a criação de tabelas e o estabelecimento de relações entre essas tabelas de acordo com as regras projetadas para proteger os dados e tornar o Banco de Dados mais flexível, eliminando a redundância e a dependência inconsistente.

Desnormalização, por sua vez, é uma técnica aplicada a bancos de dados relacionais com o objetivo de otimizar a performance de consultas que envolvem muitas tabelas. Esse tipo de consulta normalmente requer a utilização de junções (JOINS) entre tabelas para obter todos os dados necessários, o que acaba comprometendo o desempenho do banco de dados.

Para contornar esse problema em casos específicos pode ser viável desnormalizar o banco, juntando os dados em uma única tabela (ou menos tabelas do que as que eram usadas originalmente). Apesar de isso acabar gerando redundância de informações, as aplicações serão beneficiadas com o ganho de desempenho devido a não ser mais necessário unir várias tabelas.

O sWarden não faz uso da desnormalização, porquanto a performance do Postgres enquanto estruturado já entrega os resultados desejados e esperados, portanto, não há redundância de dados.

## Consultas e Transações

O uso de índices em chaves primárias e estrangeiras acelera as operações de leitura. As consultas são projetadas para aproveitar esses índices, evitando full table scans sempre que possível.

Quanto às transações, o PostgreSQL é perfeitamente capaz de garantir com excelência os quatro atributos ACID: atomicidade, consistência, isolamento e durabilidade. Isso é crítico para operações que envolvem múltiplas tabelas e para a manutenção da integridade dos dados em cenários de concorrência. Também utilizado nos testes, seção detalhada a seguir.

## Testes

Esta seção abrange os testes de Banco de Dados para os modelos `Credential`, `Card` e `SecurityNote`, garantindo a integridade, validação e armazenamento correto dos dados no Banco de Dados.

O uso de atomicidade aqui se apresenta em momentos onde falhas são esperadas e o PostgreSQL deve retornar um erro. Quando esperado, esse erro está pronto para ser tratado dentro da aplicação. Nos testes, a ideia é exatamente mapear os modelos de modo que alterações nas demais partes da aplicação não venham remover uma regra ou alterar determinado comportamento que não tenha sido antes tratado ou que de alguma forma seja esperado.

A importância desse controle é demonstrada em momentos que os modelos dentro da aplicação possuem seus campos (colunas) editados mas não totalmente tratados nas funções "handlers".

Os testes a seguir focam nas interações com o Banco de Dados e representam os três modelos, restrições e exceções relacionadas a esses modelos.

1. Validade da Instância:
    
    Verifica se as instâncias do modelo criadas no Banco de Dados são da classe correta.
    
    Método de Teste: `test_[Credential/Card/SecurityNote]_instance_validity`

1. Atribuição de Valor Chave:
    
    Valida se os atributos de uma instância do modelo são atribuídos corretamente.
    
    Método de Teste: `test_[Credential/Card/SecurityNote]_key_value_assertion`

1. Validade de Chave Estrangeira:
    
    Verifica a validade do relacionamento de chave estrangeira entre Credential e User.
    
    Método de Teste: `test_[Credential/Card/SecurityNote]_user_foreign_key_validity`

1. Integridade e Validação na Criação:
    
    Testa a integridade e validação da criação do modelo no Banco de Dados.
    
    Método de Teste: `test_[Credential/Card/SecurityNote]_create_validity`

1. Integridade e Validação na Atualização:
    
    Garante que as atualizações em instâncias do modelo mantenham a integridade e validação dos dados.
    
    Método de Teste: `test_[Credential/Card/SecurityNote]_update_validity`

1. Integridade na Exclusão:
    
    Valida a exclusão correta de instâncias do modelo no Banco de Dados.
    
    Método de Teste: `test_[Credential/Card/SecurityNote]_delete_validity`

1. Tratamento de Exceções:
    
    Testa o tratamento correto de exceções e erros de validação durante a criação do modelo.
    
    Método de Teste: `test_[Credential/Card/SecurityNote]_db_exception_raises`
