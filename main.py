from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated
from database import criar_tabela, criar_tabela_usuarios, listar_produtos, buscar_produtos_nome, adicionar_produto, buscar_produto_id, atualizar_produto_db, excluir_produto_db, buscar_produtos_estoque, buscar_usuario_username, verificar_senha
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title='API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342", "https://pedrosilva370.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

criar_tabela()
criar_tabela_usuarios()
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")

class ProdutoCriacao(BaseModel):
    nome: Annotated[str, Field(min_length=3, max_length=50, description="Nome do produto")]
    preco: Annotated[float, Field(gt=0, le=10000, description="Preço do produto em reais")]
    estoque: Annotated[int, Field(ge=0, description="Quantidade disponível em estoque")]

class ProdutoResposta(BaseModel):
    id: Annotated[int, Field(ge=0, description="ID do produto")]
    nome: Annotated[str, Field(min_length=3, max_length=50, description="Nome do produto")]
    preco: Annotated[float, Field(gt=0, le=10000, description="Preço do produto em reais")]
    estoque: Annotated[int, Field(ge=0, description="Quantidade disponível em estoque")]

class Login(BaseModel):
    username: str
    senha: str

def criar_token(username):
    return jwt.encode({'sub': username}, SECRET_KEY, algorithm='HS256')

def verificar_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def verificar_autenticacao(credentials = Depends(security)):
    token = credentials.credentials
    return verificar_token(token)

@app.get('/')
def inicio():
    return {'message': 'API funcionando!'}

@app.post('/login')
def login(dados: Login):
    usuario = buscar_usuario_username(dados.username)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    if not verificar_senha(dados.senha, usuario["senha"]):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    return criar_token(dados.username)

@app.get('/produtos', response_model=list[ProdutoResposta])
def produtos(nome=None):
    if nome is None:
        return listar_produtos()
    else:
        resultado = buscar_produtos_nome(nome)
        if resultado:
            return resultado
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.get('/produtos/{id}', response_model=ProdutoResposta)
def produto(id: int):
    resultado = buscar_produto_id(id)
    if resultado:
        return resultado
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.get('/sobre')
def sobre(usuario = Depends(verificar_autenticacao)):
    return {"nome": "API REST de Loja", "versao": "1.0"}

@app.post('/produtos', response_model=ProdutoResposta)
def criar_produto(produto: ProdutoCriacao, usuario = Depends(verificar_autenticacao)):
    novo_produto = adicionar_produto(produto.nome, produto.preco, produto.estoque)
    return buscar_produto_id(novo_produto)

@app.put('/produtos/{id}', response_model=ProdutoResposta)
def atualizar_produto(id:int, novo_produto: ProdutoCriacao, usuario = Depends(verificar_autenticacao)):
    resultado = buscar_produto_id(id)
    if resultado:
        atualizar_produto_db(id, novo_produto.nome, novo_produto.preco, novo_produto.estoque)
        return buscar_produto_id(id)
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete('/produtos/{id}')
def excluir_produto(id:int, usuario = Depends(verificar_autenticacao)):
    resultado = buscar_produto_id(id)
    if resultado:
        excluir_produto_db(id)
        return {'message': 'Produto excluído com sucesso!'}
    return {'message': 'Produto não encontrado'}

@app.get('/produtos/estoque/{quantidade}')
def armazenamento(quantidade: int):
    resultado = buscar_produtos_estoque(quantidade)
    if resultado:
        return resultado
    return {'message': 'Nenhum produto encontrado com essa quantidade de estoque'}
