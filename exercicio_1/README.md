# Desafio 1 de Web Services RESTful com Flask, PostgreSQL e ElephantSQL

## Objetivo
Neste desafio, você desenvolverá um sistema completo de vendas online, abrangendo clientes, produtos, estoque, carrinhos de compras e pedidos. Implementando RESTful Web Services com Flask e PostgreSQL na ElephantSQL, seu objetivo é construir uma API RESTful robusta, aplicando os princípios do Nível 2 do Modelo de Maturidade de Richardson.

## Requisitos do Sistema

### Estrutura do Projeto
Mantenha uma estrutura de projeto limpa e organizada, dividida em:
- Código (incluindo `app.py` e módulos Python adicionais).
- Coleção Postman (`postman_collection.json`).
- Documentação da API (recomendada).

### Modelagem Relacional
Desenvolva um esquema de banco de dados relacional no PostgreSQL com as seguintes entidades e atributos:

#### Entidades
- **Clientes**: `id` (auto incremento), `nome`, `email` (único), `cpf` (único), `senha`.
- **Produtos**: `id` (auto incremento), `nome`, `descricao`, `preco`, `estoque`.
- **Fornecedores**: `id` (auto incremento), `nome`, `email` (único), `cnpj` (único).
- **Estoque_Fornecedor**: `produto_id`, `fornecedor_id`, `quantidade`, `preco_custo`.
- **Carrinho**: `id` (auto incremento), `cliente_id`, `produto_id`, `quantidade`.
- **Pedido**: `id` (auto incremento), `cliente_id`, `data_hora`, `valor_total`, `status` (`pendente`, `aprovado`, `cancelado`, `entregue`). 

### Implementação da API RESTful

#### Endpoints e Verbos HTTP

- **Clientes**
  - `GET /clientes`: Lista todos os clientes. OK  
  - `POST /clientes`: Cria um novo cliente. OK
  - `GET /clientes/{id}`: Detalhes do cliente. OK
  - `PUT /clientes/{id}`: Atualiza cliente. OK
  - `DELETE /clientes/{id}`: Exclui cliente. OK

- **Produtos**
  - `GET /produtos`: Lista todos os produtos. OK
  - `POST /produtos`: Cria novo produto. OK 
  - `GET /produtos/{id}`: Detalhes do produto. OK
  - `PUT /produtos/{id}`: Atualiza produto. OK
  - `DELETE /produtos/{id}`: Exclui produto. OK

- **fornecedores**
  - `GET /fornecedores`: Lista todos os fornecedores. OK
  - `POST /fornecedores`: Cria novo fornecedores. OK
  - `GET /fornecedores/{id}`: Detalhes do fornecedores. OK
  - `PUT /fornecedores/{id}`: Atualiza fornecedores. OK
  - `DELETE /fornecedores/{id}`: Exclui fornecedores. OK

- **Carrinho** `relacional`
  - `POST /carrinho`: Adiciona item ao carrinho.
  - `PUT /carrinho/{id}`: Atualiza item no carrinho.
  - `DELETE /carrinho/{id}`: Remove item do carrinho.

- **Pedidos** `relacional`
  - `GET /pedidos`: Lista pedidos do cliente.
  - `POST /pedidos`: Cria novo pedido.
  - `GET /pedidos/{id}`: Detalhes do pedido.

- **Pense e crie o restante das especificações de rota dos recursos não listado acima**


#### Relacionamentos e Restrições:

- Um cliente pode ter vários pedidos.
- Um produto pode ter vários fornecedores.
- Um fornecedor pode fornecer vários produtos.
- Um pedido pode ter vários itens (relacionamento com Carrinho).


#### Códigos de Status HTTP

Use os códigos de status HTTP corretamente para indicar o resultado de cada operação (200, 201, 400, 404, 500).

#### Validação de Campos

Valide campos obrigatórios e opcionais, fornecendo feedback claro ao usuário.

#### Atualizações Parciais

Permita atualizações parciais de recursos nos endpoints apropriados.

### Deploy

Realize o deploy de sua API na Heroku ou outra plataforma de nuvem.

#### Filtros e Ordenação

Implemente filtros e ordenação nos endpoints de listagem.

#### Imagens para Produtos (totalmente opcional)

Adicione suporte a imagens nos produtos.

#### Sistema de Notificações (totalmente opcional)

Crie notificações por email para pedidos. Dica: Pesquise "enviar email gmail flask".

## Tutoriais e Recursos

Aqui estão alguns recursos que podem ajudá-lo a completar este desafio:

## Fonte de Informação

### Notion da dicplina: 
- https://slender-ceder-1da.notion.site/a09548d285554638af41c2ad3989b79f?v=c25df69714e94eb1aca7df10cebb9ec7&pvs=4


### Ajuda com a plataforma ElephantSQL

- Introdução e Configurações Iniciais: https://www.elephantsql.com/blog/databases-for-beginners-what-is-a-database-what-is-postgresql.html

- Conectando o pgAdmin ao seu server Elephant: https://www.elephantsql.com/docs/pgadmin.html

- Documentação oficial: https://www.elephantsql.com/docs/index.html

### Ajuda com pgAdmin

- Introdução ao pgAdmin: https://www.w3schools.com/postgresql/postgresql_pgadmin4.php

- Documentação oficial: https://www.pgadmin.org/docs/pgadmin4/8.3/index.html

### Ajuda com o Python utilizando a base PostgreSql (psycog2)

- Tutorial excelente sobre psycog2: https://www.tutorialspoint.com/postgresql/postgresql_python.htm

- Documentação oficial: https://www.psycopg.org/docs/

### Ajuda com Flask

- Intro: https://www.tutorialspoint.com/flask/flask_application.htm

- Recebendo JSON via requisição: https://stackabuse.com/how-to-get-and-parse-http-post-body-in-flask-json-and-form-data/

- Variáveis na URL (urls dinâmicas): https://www.geeksforgeeks.org/generating-dynamic-urls-in-flask/

- Query Parameters: https://stackabuse.com/get-request-query-parameters-with-flask/

- Documentação oficial: https://flask.palletsprojects.com/en/3.0.x/

### Ajuda com Postman

- Intro: https://learning.postman.com/docs/getting-started/first-steps/sending-the-first-request/

- Importando uma collection: https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/


### Ajuda com Heroku

- Criando conta estudante no Heroku (precisa de cartão): https://youtu.be/aSdx43pesV4?si=PvvuopBh5rUpMa2R
- Fazendo deploy no Heroku: https://youtu.be/OU_Fqt1pBPM?si=F4jPWgEXyigcIYBQ
- Deploy de Flask no Heroku - Alt 1: https://github.com/datademofun/heroku-basic-flask 

## Conclusão

Este desafio é uma oportunidade excelente para aprimorar suas habilidades de desenvolvimento de Web Services RESTful com tecnologias modernas. Esperamos que você encontre este projeto não apenas educativo, mas também agradável. Boa sorte!

## Observações

- Adapte o desafio conforme necessário, focando no aprendizado e na aplicação de boas práticas.
- Priorize a clareza e a segurança em sua implementação.
- Use este desafio como uma chance para explorar novas ferramentas e técnicas.
