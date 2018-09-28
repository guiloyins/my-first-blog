# api-doc
Documentação do serviço API Marketplace para integração na [Júlia Kastrup]


### Sobre a API

O serviço de API da [Júlia Kastrup] fornece uma forma alternativa de criar, atualizar e remover produtos na EV, além de também receber e enviar informações de pedidos.


### Modo de usar

Todos os métodos da nossa API esperam um token de autenticação, válido por 24h. Para obtê-lo, é necessário seguir o passo abaixo:

```curl -X POST --data “email=email&password=senha” https://api-marketplace.estantevirtual.com.br/auth/login```

O retorno deve ser um hash com o valor do auth_token. Exemplo:

`{“auth_token”:“eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1MDc4MjYzMTd9.6jV-bb3C5oV-0e4CcJ212Yr1DfROgBlovkFdisc8tC0”}`


### Endpoints

- Autenticação (POST):
`https://api-marketplace.estantevirtual.com.br/auth/login`

- Criação de Produto (POST):
`https://api-marketplace.estantevirtual.com.br/produtos`

- Atualização de Produto (PUT):
`https://api-marketplace.estantevirtual.com.br/produtos`

- Atualização de Estoque (PUT):
`https://api-marketplace.estantevirtual.com.br/estoques`

- Atualização de Preço (PUT):
`https://api-marketplace.estantevirtual.com.br/precos`

Além desses pontos, usamos endpoints do lado dos vendedores para que possamos fazer `POST` de pedidos e `PUT` de status de cada pedido.



### Envio de produtos

Endpoint que recebe os dados dos títulos que devem ser preenchidos na entidade `catalogo`. Esses títulos devem ser armazenados localmente. A estrutura de dados deve prever armazenar preços também (com seu histórico, para consultas futuras).
Caso o produto já exista, a API deve permitir que seus dados sejam atualizados.

##### POST ou PUT Produtos (Vendedor / Integrador -> EV):


```
{
  "produtos": [
    {
      "categoria": "critica literaria",
      "categoria_id": 21,
      "autores": ["Autor 1","Aautor 2"],
      "codigo": "123456",
      "id_vendedor": 2124720,
      "marca": "livro_teste",
      "nome": "Meu livro de teste",
      "skus": [
        {
          "nome": "Meu livro de teste",
          "codigo": "123456",
          "marca": "livro_teste",
          "descricao": "Descrição teste para o produto teste Livro",
          "isbn": "9788506082096",
          "altura": "20.00",
          "comprimento": "20.00",
          "largura":"25.00",
          "peso":"200",
          "idioma": "Pt",
"imagens":["https:\/\/images-na.ssl-images-amazon.com\/images\/I\/91xWp9kdIDL._SX355_.jpg"],
          "status": "Ativo",
          "estoque": "1",
          "valor_de": "17.0",
          "valor_por": "7.0",
          "ano": 2018
        }
      ]
    }
  ]
}
```

Campos: 

- categoria: [nome da Estante utilizada na [Júlia Kastrup]](https://www.estantevirtual.com.br/conteudo/lista-estantes)
- **categoria_id**: ID da categoria na [Júlia Kastrup]
- **autores**: autor ou autores do livro
- **codigo**: identificador do produto no vendedor
- **id_vendedor**: ID do vendedor na [Júlia Kastrup]
- **marca**: editora do livro
- **nome**: título do livro
- **descricao**: estado de conservação do livro ou, em caso de livros novos, sinopse.
- **isbn**: isbn do livro
- altura: altura do exemplar em centímetros
- comprimento: comprimento do exemplar em centímetros
- largura: largura do exemplar em centímetros
- **peso**: peso do exemplar em gramas
- idioma: código do idioma do exemplar, de acordo com listagem abaixo.
- imagens: url da imagem de capa
- status: status do exemplar
- **estoque**: quantidade de exemplares disponíveis
- **valor_de**: preço antigo
- **valor_por**: preço atual (em caso de primeiro valor, basta colocar o mesmo nos dois campos) 
- **ano**: ano de lançamento da edição do exemplar

_Campos em negrito são de preenchimento obrigatório._ 

###### Códigos de idiomas aceitos:

- "De" = Alemão
- "Ch" = Chinês
- "Co" = Coreano
- "Da" = Dinamarquês
- "Es" = Espanhol
- "Fr" = Francês
- "El" = Grego
- "He" = Hebraico
- "Ho" = Holandês
- "Hu" = Húngaro
- "En" = Inglês
- "It" = Italiano
- "Jp" = Japonês
- "La" = Latim
- "Pl" = Polonês
- "Pt" = Português
- "Ru" = Russo

_Por padrão, esse campo é definido como "Pt", caso seja nulo._


### Atualizar preços
_Endpoint que recebe codigo_f1 e o valor do produto e:_

- Verifica se o produto existe na base local da api_marketplace
  - Caso não exista, retorna erro
  - Caso exista:
    - Atualiza o preço do produto na base de dados local
    - Chama api do nosso serviço que faz update do preço de todos itens ativos na tabela catalogo do evmain do vendedor em questão.

##### PUT Preços (F1 -> EV):

```
{
  "precos":
    [
       {
           "codigo": "PRODNORMALCOD1",
           "valor_de": 892.18,
           "valor_por": 743.48,
           "id_vendedor":3066499
       },
       {
           "codigo": "PRODNORMALCOD2",
           "valor_de": 100.18,
           "valor_por": 98.48,
           "id_vendedor":3066499
       },
    ]
}
```
Retorno:
```
{
   "success": 201
}
```
OU
```
{
   "error": 404,
   "message" : "Produto inválido."
}
```

### Atualizar estoque
_Endpoint que rece isbn e a quantidade do produto e:_ 

- Verifica se o produto existe na base local da api_marketplace
  - Caso não exista retorna erro.
  - Caso exista:
    - Caso não tenha preço vinculado retorna erro.
    - Caso exista:
      - Chama api bookshelf que retorna a quantidade de itens em estoque para o vendedor em questão
      - Caso a quantidade enviada seja maior que a quantidade no acervo:
      - Busca os dados do título e último preço na base local
      - Faz um parse dos dados para o padrão de inserção de dados do nosso serviço
      - Determina a quantidade a ser adicionada (exemplo: temos 7 no acervo e o vendedor setou a quantidade em 10 exemplares, temos que adicionar 3 exemplares na catálogo)
      - Chama api do nosso serviço e passa dados do exemplar e a quantidade.
      - Nosso serviço insere os registros e retorna sucesso ou falha. 
      - Retorna sucesso ou falha de acordo com o resultado da inserção no nosso serviço
    - Caso contrário
      - Chama a api do nosso serviço e passa o isbn e quantidade de registros a excluir.
      - Nosso serviço apaga os últimos itens cadastrados na catalogo
      - Chama api do nosso serviço que faz update do preço de todos itens ativos na tabela catalogo do evmain do vendedor em questão.

##### PUT Estoques (F1 -> EV):

```
{
  "estoques":
    [
       {
            "codigo": "PRODNORMALCOD1",
            "estoque": 144,
            "id_vendedor":3066499
       },
       {
            "codigo": "PRODNORMALCOD2",
            "estoque": 0,
            "id_vendedor":3066499
       }
    ]
}
```

Retorno:
```
{
   "success": 201
}
```
OU

```
{
   "error": 404,
   "message" : "Produto inválido."
}
```

### Atualizar pedido
Endpoint que atualiza o status de um determinado pedido:

- Recebe o ID do pedido na ev, status e o código de rastreio (se houver)
- Busca o status na EV
  - Caso o status não exista, retorna erro.
  - Caso o status exista: 
    - chama a api do nosso serviço passando id do pedido, status e o código de rastreio (se houver)
    - Retorna sucesso ou erro de acordo com o que o nosso serviço retornar.


##### PUT Pedido sentido (EV -> F1 e F1 -> EV)

```
{
  "pedido":
    {
    "id_vendedor": 2124720,
    "marketplace_id_pedido": 101,
    "status_codigo" : "[STATUS_DO_PEDIDO]",                    # status aceitos: NEW | APPROVED | CANCELED | SHIPPED
    "razao_cancelamento" : "Campo preenchido se necessário",   # deve ser preenchido no envio do status CANCELED
    "rastreio" : "codigo de rastreio correios",                # deve ser preenchido no envio do status SHIPPED, quando a entrega for via Correios 
    "url_rastreio":"url da transportadora"                     # deve ser preenchido  no envio do status SHIPPED, quando a entrega for via transportadora 

    }
}
```

Retorno:

```
{
   "success": 200,
}
```

OU

```{
   "error": 400,
   "message" : "Status inválido."
}
```


### Enviar pedidos

De 5 em 5 minutos nós devemos fazer um pooling e mandar os pedidos em standby desde a última vez que enviamos dados com sucesso.

- Busca pedidos em standby por data do Roma

Para cada pedido:
- Busca os dados do cliente
- Chama o post_pedido

##### POST pedido (EV -> F1):

```
{ 
   "id_vendedor":"340690",
   "pedidos":[ 
      { 
         "id_cliente":3030537,
         "transportadora":"normal",
         "marketplace_id_pedido":27596692,
         "marketplace_store":"estantevirtual",
         "parcelas":1,
         "status_codigo":"PROCESSING",
         "marketplace_data_pedido": '2018-04-25 00:00:00',
         "data_estimada_entrega": '2018-05-06 00:00:00',
         "valor_total_pedido":"38.42",
         "valor_total_frete":9.42,
         "valor_total_desconto":0,
         "cliente":{ 
            "tipo":"PF",
            "razao_social":"Ana Silva",
            "cpf_cnpj":"05773931702",
            "email":"asilva@google.com.br",
            "data_aniversario":nil,
            "telefone1":"21 23456781"
         },
         "endereco":{ 
            "tipo_endereco":"Entrega",
            "nome_destinatario":"Ana Silva",
            "estado":"Rio de Janeiro",
            "cidade":"Rio de Janeiro",
            "bairro":"Centro",
            "logradouro":"Rua Maricá",
            "numero":"0",
            "complemento":"ap 101",
            "cep":"22220-010"
         },
         "produtos":[ 
            { 
               "codigo":"1670133",
               "quantidade":1,
               "valor":"29.0",
               "desconto":0
            }
         ]
      }
   ]
}
``` 
 
Retorno:

```
{
   "success": 201,
   "id_pedido": 20
}
```