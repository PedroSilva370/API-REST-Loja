// ====================
// LOGIN
// ====================

let botaoEntrar = document.getElementById("entrar");

botaoEntrar.addEventListener("click", function() {

    let username = document.getElementById("username").value;
    let senha = document.getElementById("senha").value;

    fetch("https://api-rest-loja.onrender.com/login", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            username: username,
            senha: senha
        })

    })
    .then(resposta => {

        if (!resposta.ok) {
            throw new Error("Usuário ou senha inválidos");
        }

        return resposta.json();

    })
    .then(token => {

        localStorage.setItem("token", token);

        document.getElementById("mensagem").textContent =
            "Login realizado com sucesso!";

        console.log("Token recebido:", token);

    })
    .catch(erro => {

        document.getElementById("mensagem").textContent =
            "Erro: " + erro.message;

        console.log("Erro no login:", erro);

    });

});


// ====================
// CARREGAR PRODUTOS
// ====================

let botaoProdutos = document.getElementById("carregarProdutos");
let areaProdutos = document.getElementById("produtos");

function carregarProdutos() {

    fetch("https://api-rest-loja.onrender.com/produtos")

        .then(resposta => resposta.json())

        .then(listaProdutos => {

            console.log("Produtos recebidos:", listaProdutos);

            areaProdutos.innerHTML = "";

            listaProdutos.forEach(produto => {

                let elemento = document.createElement("div");

                elemento.classList.add("produto");

                elemento.innerHTML = `
                    <h3>${produto.nome}</h3>
                    <p><strong>ID:</strong> ${produto.id}</p>
                    <p><strong>Preço:</strong> R$ ${produto.preco}</p>
                    <p><strong>Estoque:</strong> ${produto.estoque}</p>
                `;

                areaProdutos.appendChild(elemento);

            });

        })

        .catch(erro => {

            console.log("Erro:", erro);

        });

}

botaoProdutos.addEventListener("click", function() {

    carregarProdutos();

});


// ====================
// CADASTRAR PRODUTO
// ====================

let botaoCadastrar = document.getElementById("cadastrarProduto");

botaoCadastrar.addEventListener("click", function() {

    let nome = document.getElementById("nomeProduto").value;
    let preco = Number(document.getElementById("precoProduto").value);
    let estoque = Number(document.getElementById("estoqueProduto").value);

    let token = localStorage.getItem("token");

    fetch("https://api-rest-loja.onrender.com/produtos", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",
            "Authorization": "Bearer " + token

        },

        body: JSON.stringify({

            nome: nome,
            preco: preco,
            estoque: estoque

        })

    })

    .then(resposta => resposta.json())

    .then(dados => {

        console.log("Produto cadastrado:", dados);

        carregarProdutos();

    })

    .catch(erro => {

        console.log("Erro:", erro);

    });

});


// ====================
// EDITAR PRODUTO
// ====================

let botaoEditar = document.getElementById("editarProduto");

botaoEditar.addEventListener("click", function() {

    let id = document.getElementById("idProdutoEditar").value;
    let nome = document.getElementById("nomeProdutoEditar").value;
    let preco = Number(document.getElementById("precoProdutoEditar").value);
    let estoque = Number(document.getElementById("estoqueProdutoEditar").value);

    let token = localStorage.getItem("token");

    fetch("https://api-rest-loja.onrender.com/produtos/" + id, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json",
            "Authorization": "Bearer " + token

        },

        body: JSON.stringify({

            nome: nome,
            preco: preco,
            estoque: estoque

        })

    })

    .then(resposta => resposta.json())

    .then(dados => {

        console.log("Produto atualizado:", dados);

        carregarProdutos();

    })

    .catch(erro => {

        console.log("Erro:", erro);

    });

});


// ====================
// EXCLUIR PRODUTO
// ====================

let botaoExcluir = document.getElementById("excluirProduto");

botaoExcluir.addEventListener("click", function() {

    let id = document.getElementById("idProdutoExcluir").value;

    let token = localStorage.getItem("token");

    fetch("https://api-rest-loja.onrender.com/produtos/" + id, {

        method: "DELETE",

        headers: {

            "Authorization": "Bearer " + token

        }

    })

    .then(resposta => resposta.json())

    .then(dados => {

        console.log("Produto excluído:", dados);

        carregarProdutos();

    })

    .catch(erro => {

        console.log("Erro:", erro);

    });

});