# API REST de Loja

*A full-stack Store REST API — backend built from scratch in Python, frontend assembled with AI assistance.*

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791)
![Status](https://img.shields.io/badge/status-em%20produção-brightgreen)
![License](https://img.shields.io/badge/license-não%20definida-lightgrey)

## Visão Geral

O **API REST de Loja** é um projeto full-stack desenvolvido para simular o backend e a interface de gerenciamento de produtos de uma loja.

O projeto foi construído com foco em desenvolvimento de APIs REST, persistência de dados, autenticação, validação, integração entre frontend e backend e deploy em produção. A aplicação começou como uma API simples em Python e evoluiu progressivamente até se tornar uma aplicação completa, com backend REST, banco de dados relacional, sistema de autenticação, controle de acesso via JWT, validação de dados, frontend web, comunicação assíncrona entre cliente e servidor, e hospedagem em produção.

O projeto representa uma aplicação prática dos conceitos de **arquitetura cliente-servidor**: o frontend atua como cliente, realizando requisições HTTP para o backend, que processa essas requisições, aplica regras de negócio, valida os dados e realiza as operações no banco de dados.

> **Divisão do trabalho:** todo o **backend/API** (rotas, autenticação, validação, banco de dados, regras de negócio e deploy) foi desenvolvido integralmente pelo autor deste repositório. A camada de **frontend** (HTML, CSS e JavaScript) foi construída com o auxílio de inteligência artificial, com o objetivo de complementar o projeto e demonstrar a integração completa entre cliente e servidor.

## Funcionalidades

- Cadastro, listagem, edição e exclusão de produtos (CRUD completo)
- Autenticação de usuários via JSON Web Token (JWT)
- Hash seguro de senhas com `pwdlib`
- Validação de dados de entrada com Pydantic (nome, preço e estoque de produtos)
- Documentação interativa automática via Swagger UI e ReDoc
- Controle de acesso: endpoints de escrita exigem token válido
- Interface web para login, visualização, cadastro, edição e remoção de produtos
- Comunicação assíncrona entre frontend e backend via Fetch API
- Persistência de sessão do usuário no navegador via LocalStorage
- Configuração de CORS para comunicação entre domínios distintos
- Deploy completo em produção (backend, frontend e banco de dados)

## Tecnologias Utilizadas

| Camada | Tecnologia | Função no projeto |
|---|---|---|
| Backend | Python | Linguagem principal da API |
| Backend | FastAPI (0.141.1) | Framework para construção da API REST |
| Backend | Pydantic (2.13.5) | Validação e serialização de dados |
| Backend | Uvicorn | Servidor ASGI para execução da aplicação |
| Backend | PyJWT | Geração e validação de tokens JWT |
| Backend | pwdlib | Hash seguro de senhas |
| Backend | python-dotenv | Carregamento de variáveis de ambiente |
| Banco de Dados | PostgreSQL | Banco de dados relacional utilizado em produção |
| Banco de Dados | Psycopg | Driver de conexão entre Python e PostgreSQL |
| Frontend | HTML5 | Estrutura da interface web |
| Frontend | CSS3 | Estilização e layout da aplicação |
| Frontend | JavaScript (Fetch API) | Lógica de interface e comunicação com a API |
| Infraestrutura | Render | Hospedagem do backend (API) |
| Infraestrutura | GitHub Pages | Hospedagem do frontend |
| Infraestrutura | Neon | Hospedagem do banco de dados PostgreSQL em nuvem |
| Versionamento | Git / GitHub | Controle de versão e repositório do código-fonte |

## Pré-requisitos

Para executar o projeto localmente, você precisará de:

- Python 3.10 ou superior (recomendado 3.11+; ajuste conforme a versão utilizada no seu ambiente)
- `pip` para instalação das dependências
- Git
- Um banco de dados PostgreSQL (local ou em nuvem, como o Neon) para persistência dos dados
- Um navegador atualizado para executar o frontend

## Instalação

Clone o repositório:

```bash
git clone https://github.com/PedroSilva370/API-REST-Loja.git
cd API-REST-Loja
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Instale as dependências do backend a partir do `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Arquitetura do Projeto

O diagrama abaixo resume como frontend, backend e banco de dados se comunicam em produção:

```mermaid
flowchart TD
    A[Usuário / Browser] --> B[GitHub Pages - Frontend HTML/CSS/JS]
    B -->|HTTPS / Fetch API| C[Render - Backend FastAPI]
    C -->|Autenticação JWT| C
    C -->|SQL via Psycopg| D[(Neon - PostgreSQL)]
    D --> C
    C --> B
    B --> A
```

## Configuração

O projeto utiliza variáveis de ambiente para armazenar informações sensíveis, carregadas através do `python-dotenv`. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```text
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
SECRET_KEY=sua_chave_secreta_para_geracao_do_jwt
```

Observações importantes:

- O arquivo `.env` está incluído no `.gitignore` e não deve ser versionado.
- `DATABASE_URL` deve apontar para uma instância PostgreSQL válida (local ou em nuvem, como o Neon).
- `SECRET_KEY` é utilizada na geração e validação dos tokens JWT.

## Como Executar

### Backend (modo desenvolvimento)

```bash
fastapi dev main.py
```

A API ficará disponível em `http://127.0.0.1:8000`, com documentação interativa em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Frontend

O frontend é composto por arquivos estáticos (HTML, CSS e JavaScript) e pode ser executado abrindo o arquivo principal diretamente no navegador ou através de uma extensão de servidor local (como o Live Server).

### Ambiente em Produção

O projeto já está publicado e pode ser acessado diretamente:

- **API (backend):** `https://api-rest-loja.onrender.com/`
- **Frontend (interface web):** `https://pedrosilva370.github.io/API-REST-Loja/`

## Exemplos de Uso

### Autenticação (login)

```bash
curl -X POST "https://api-rest-loja.onrender.com/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "senha": "senha123"}'
```

### Listar produtos

```bash
curl -X GET "https://api-rest-loja.onrender.com/produtos"
```

### Cadastrar um produto (endpoint protegido)

```bash
curl -X POST "https://api-rest-loja.onrender.com/produtos" \
  -H "Authorization: Bearer <seu_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Produto Exemplo", "preco": 49.90, "estoque": 10}'
```

### Consumindo a API a partir do frontend (JavaScript)

```javascript
fetch("https://api-rest-loja.onrender.com/produtos")
  .then((response) => response.json())
  .then((produtos) => console.log(produtos));
```

### Armazenamento do token no navegador

```javascript
// Após o login
localStorage.setItem("token", token);

// Em requisições protegidas
const token = localStorage.getItem("token");
```

## Contribuição

Contribuições, sugestões e correções são bem-vindas. Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua alteração (`git checkout -b minha-alteracao`)
3. Faça o commit das mudanças (`git commit -m "descrição da alteração"`)
4. Envie a branch (`git push origin minha-alteracao`)
5. Abra um Pull Request

Sinta-se à vontade também para abrir uma *issue* relatando problemas ou sugerindo melhorias.

## Licença

Este projeto ainda não possui uma licença definida. Enquanto isso, todos os direitos sobre o código-fonte permanecem reservados ao autor. Caso deseje utilizar, modificar ou distribuir este projeto, entre em contato com o autor para mais informações. A adoção futura de uma licença de código aberto (como MIT) poderá ser avaliada.

## Autor

**Pedro Silva** ([PedroSilva370](https://github.com/PedroSilva370))

O desenvolvimento completo do **backend/API** deste projeto — incluindo rotas, autenticação, validação de dados, integração com o banco de dados e deploy em produção — foi realizado integralmente pelo autor. A camada de **frontend** foi desenvolvida com o auxílio de inteligência artificial, como forma de completar a aplicação full-stack e demonstrar a integração entre cliente e servidor.

- Frontend: [pedrosilva370.github.io/API-REST-Loja](https://pedrosilva370.github.io/API-REST-Loja/)
- API em produção: [api-rest-loja.onrender.com](https://api-rest-loja.onrender.com/)
