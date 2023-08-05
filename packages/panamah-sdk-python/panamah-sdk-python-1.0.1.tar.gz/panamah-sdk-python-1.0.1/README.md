## Requisitos mínimos

- Python >= 3.4

## Instalação

1. Execute o comando

   ```bash
   pip install panamah-sdk-python
   ```

2. Utilize as APIs e modelos através do
   ```python
   from panamah_sdk.stream import PanamahStream
   from panamah_sdk.admin import PanamahAdmin
   #Todas as definições de modelos
   from panamah_sdk.models.definitions import *
   #Só algumas
   from panamah_sdk.models.definitions import PanamahProduto, PanamahSecao
   ```

## Exemplo de uso da API administrativa

```python
from panamah_sdk.admin import PanamahAdmin
from panamah_sdk.exceptions import NotFoundException
from panamah_sdk.models.definitions import PanamahAssinante

admin = PanamahAdmin()

try:
    assinante = admin.get_assinante('21705632000120')
    print(assinante)
except NotFoundException:
        #instanciando um modelo de assinante
        assinante = PanamahAssinante(
            id='21705632000120',
            fantasia='Supermercado Exemplo',
            nome='Supermercado Exemplo Ltda',
            bairro='Rua Poebla',
            cidade='Caucaia',
            uf='CE'
        )
        #criando o assinante no Panamah
        created_assinante = admin.create_assinante(assinante)
        print(created_assinante)
```

## Exemplo de uso da API de streaming

```python
from panamah_sdk.stream import PanamahStream
from panamah_sdk.models.definitions import PanamahProduto, PanamahProdutoComposicao, PanamahProdutoComposicaoItem, PanamahProdutoFornecedor
from datetime import datetime
from os import environ

#inicializando a api de streaming
stream = PanamahStream(
    assinante_id= '21705632000120',
    authorization_token= environ.get('PANAMAH_AUTHORIZATION_TOKEN'), #(opcional) caso não seja passado, é considerado a variável de ambiente PANAMAH_AUTHORIZATION_TOKEN
    secret= environ.get('PANAMAH_SECRET'), #(opcional) caso não seja passado, é considerado a variável de ambiente PANAMAH_SECRET
)

def before_save(model, prevent_save):
    print('Model', model)
    #prevent_save() #essa linha cancelaria o salvamento

stream.on('before_save', before_save)

def before_delete(model, prevent_delete):
    print('Model', model)
    #prevent_delete() #essa linha cancelaria a deleção

stream.on('before_delete', before_delete)

produto = PanamahProduto(
    id= '1111',
    descricao= 'Coca-cola',
    data_inclusao= datetime.now(),
    secao_id= '999',
    composicao= PanamahProdutoComposicao(
        quantidade= 2,
        itens= [
            PanamahProdutoComposicaoItem(
                produto_id= '432',
                quantidade= 1
            ),
            PanamahProdutoComposicaoItem(
                produto_id= '567',
                quantidade= 1
            )
        ]
    ),
    fornecedores= [
        PanamahProdutoFornecedor(
            id= '222',
            principal= True
        )
    ]
)

try:
    stream.save(produto)
except ValueError as e: 
    print(e) #erro na validação do modelo

stream.delete(produto)

#sempre chamar antes de finalizar a aplicação
stream.flush()
```

## Exemplo de uso da API de streaming com multitenancy

```python
from panamah_sdk.stream import PanamahStream
from panamah_sdk.models.definitions import PanamahProduto, PanamahProdutoComposicao, PanamahProdutoComposicaoItem, PanamahProdutoFornecedor
from datetime import datetime
from os import environ

#inicializando a api de streaming
stream = PanamahStream(
    authorization_token= environ.get('PANAMAH_AUTHORIZATION_TOKEN'), #(opcional) caso não seja passado, é considerado a variável de ambiente PANAMAH_AUTHORIZATION_TOKEN
    secret= environ.get('PANAMAH_SECRET'), #(opcional) caso não seja passado, é considerado a variável de ambiente PANAMAH_SECRET
)

def before_save(model, prevent_save):
    print('Model', model)
    #prevent_save() #essa linha cancelaria o salvamento

stream.on('before_save', before_save)

def before_delete(model, prevent_delete):
    print('Model', model)
    #prevent_delete() #essa linha cancelaria a deleção

stream.on('before_delete', before_delete)

produto = PanamahProduto(
    id= '1111',
    descricao= 'Coca-cola',
    data_inclusao= datetime.now(),
    secao_id= '999',
    composicao= PanamahProdutoComposicao(
        quantidade= 2,
        itens= [
            PanamahProdutoComposicaoItem(
                produto_id= '432',
                quantidade= 1
            ),
            PanamahProdutoComposicaoItem(
                produto_id= '567',
                quantidade= 1
            )
        ]
    ),
    fornecedores= [
        PanamahProdutoFornecedor(
            id= '222',
            principal= True
        )
    ]
)

try:
    stream.save(produto, '21705632000120') #salvando para o primeiro assinante
    stream.save(produto, '00934509022') #salvando para o segundo
except ValueError as e: 
    print(e) #erro na validação do modelo

stream.delete(produto, '21705632000120') #deletando para o primeiro assinante
stream.delete(produto, '00934509022') #deletando para o segundo

#sempre chamar antes de finalizar a aplicação
stream.flush()
```
