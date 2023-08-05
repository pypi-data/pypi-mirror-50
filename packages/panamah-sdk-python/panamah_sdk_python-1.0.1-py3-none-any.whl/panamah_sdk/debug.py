from .stream import PanamahStream
from .models.definitions import PanamahProduto, PanamahProdutoComposicao, PanamahProdutoComposicaoItem, PanamahProdutoFornecedor
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