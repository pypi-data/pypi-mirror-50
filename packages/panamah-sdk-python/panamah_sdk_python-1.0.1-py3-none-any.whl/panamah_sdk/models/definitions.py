from .base import Model, StringField, NumberField, BooleanField, DateField, ObjectField, StringListField, ObjectListField


class PanamahAssinante(Model):
    name = 'ASSINANTE'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'fantasia': StringField(required=True),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'revenda_id': StringField(required=False, json_name='revendaId'),
        'bairro': StringField(required=True),
        'softwares_ativos': StringListField(required=True, allowedValues=['MILENIO', 'SYSPDV', 'VAREJOFACIL', 'SYSPDVWEB', 'EASYASSIST', 'SYSPDV_APP', 'COLETOR'], json_name='softwaresAtivos'),
        'softwares_em_contratos_de_manutencao': StringListField(required=True, allowedValues=['MILENIO', 'SYSPDV', 'VAREJOFACIL', 'SYSPDVWEB', 'EASYASSIST', 'SYSPDV_APP', 'COLETOR']),
        'series': StringListField(required=False),
        'ativo': BooleanField(required=True, default=True)
    }


class PanamahRevenda(Model):
    name = 'REVENDA'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'fantasia': StringField(required=True),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True)
    }


class PanamahSecao(Model):
    name = 'SECAO'
    schema = {
        'id': StringField(required=True),
        'codigo': StringField(required=True),
        'descricao': StringField(required=True)
    }


class PanamahGrupo(Model):
    name = 'GRUPO'
    schema = {
        'id': StringField(required=True),
        'codigo': StringField(required=True),
        'descricao': StringField(required=True),
        'secao_id': StringField(required=True, json_name='secaoId')
    }


class PanamahSubgrupo(Model):
    name = 'SUBGRUPO'
    schema = {
        'id': StringField(required=True),
        'codigo': StringField(required=True),
        'descricao': StringField(required=True),
        'secao_id': StringField(required=True, json_name='secaoId'),
        'grupo_id': StringField(required=True, json_name='grupoId')
    }


class PanamahHolding(Model):
    name = 'HOLDING'
    schema = {
        'id': StringField(required=True),
        'descricao': StringField(required=True)
    }


class PanamahLoja(Model):
    name = 'LOJA'
    schema = {
        'ativa': BooleanField(required=True),
        'id': StringField(required=True),
        'descricao': StringField(required=True),
        'numero_documento': StringField(required=True, json_name='numeroDocumento'),
        'matriz': BooleanField(required=True),
        'holding_id': StringField(required=True, json_name='holdingId'),
        'ramo': StringField(required=True),
        'logradouro': StringField(required=False),
        'numero': StringField(required=False),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True),
        'cep': StringField(required=False),
        'distrito': StringField(required=False),
        'complemento': StringField(required=False),
        'telefone': StringField(required=False),
        'qtd_checkouts': NumberField(required=False, json_name='qtdCheckouts'),
        'area_m_2': NumberField(required=False, json_name='areaM2'),
        'qtd_funcionarios': NumberField(required=False, json_name='qtdFuncionarios')
    }


class PanamahMeta(Model):
    name = 'META'
    schema = {
        'id': StringField(required=True),
        'mes': NumberField(required=True),
        'ano': NumberField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'secao_id': StringField(required=True, json_name='secaoId'),
        'valor': NumberField(required=True)
    }


class PanamahFormaPagamento(Model):
    name = 'FORMA_PAGAMENTO'
    schema = {
        'id': StringField(required=True),
        'descricao': StringField(required=True)
    }


class PanamahFuncionario(Model):
    name = 'FUNCIONARIO'
    schema = {
        'data_nascimento': DateField(required=False, json_name='dataNascimento'),
        'id': StringField(required=True),
        'login': StringField(required=False),
        'nome': StringField(required=True),
        'numero_documento': StringField(required=False, json_name='numeroDocumento'),
        'ativo': BooleanField(required=True),
        'senha': StringField(required=False),
        'loja_ids': StringListField(required=False, json_name='lojaIds')
    }


class PanamahAcesso(Model):
    name = 'ACESSO'
    schema = {
        'id': StringField(required=True),
        'funcionario_ids': StringListField(required=True, json_name='funcionarioIds')
    }


class PanamahCliente(Model):
    name = 'CLIENTE'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'numero_documento': StringField(required=True, json_name='numeroDocumento'),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True)
    }


class PanamahFornecedor(Model):
    name = 'FORNECEDOR'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'numero_documento': StringField(required=True, json_name='numeroDocumento'),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True)
    }


class PanamahProdutoFornecedor(Model):
    schema = {
        'id': StringField(required=True),
        'principal': BooleanField(required=True)
    }


class PanamahProdutoComposicaoItem(Model):
    schema = {
        'produto_id': StringField(required=True, json_name='produtoId'),
        'quantidade': NumberField(required=True)
    }


class PanamahProdutoComposicao(Model):
    schema = {
        'itens': ObjectListField(required=False, object_class=PanamahProdutoComposicaoItem),
        'quantidade': NumberField(required=True)
    }


class PanamahProduto(Model):
    name = 'PRODUTO'
    schema = {
        'composicao': ObjectField(required=False, object_class=PanamahProdutoComposicao),
        'tipo_composicao': StringField(required=False, json_name='tipoComposicao'),
        'descricao': StringField(required=True),
        'data_inclusao': DateField(required=False, json_name='dataInclusao'),
        'finalidade': StringField(required=False),
        'ativo': BooleanField(required=False),
        'grupo_id': StringField(required=False, json_name='grupoId'),
        'id': StringField(required=True),
        'peso_variavel': BooleanField(required=False, json_name='pesoVariavel'),
        'quantidade_itens_embalagem': NumberField(required=False, json_name='quantidadeItensEmbalagem'),
        'secao_id': StringField(required=True, json_name='secaoId'),
        'subgrupo_id': StringField(required=False, json_name='subgrupoId'),
        'fornecedores': ObjectListField(required=False, object_class=PanamahProdutoFornecedor)
    }


class PanamahEan(Model):
    name = 'EAN'
    schema = {
        'id': StringField(required=True),
        'produto_id': StringField(required=True, json_name='produtoId'),
        'tributado': BooleanField(required=False)
    }


class PanamahTrocaFormaPagamento(Model):
    name = 'TROCA_FORMA_PAGAMENTO'
    schema = {
        'autorizador_id': StringField(required=False, json_name='autorizadorId'),
        'data': DateField(required=True),
        'forma_pagamento_destino_id': StringField(required=True, json_name='formaPagamentoDestinoId'),
        'forma_pagamento_origem_id': StringField(required=True, json_name='formaPagamentoOrigemId'),
        'id': StringField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'venda_id': StringField(required=False, json_name='vendaId'),
        'operador_id': StringField(required=False, json_name='operadorId'),
        'sequencial_pagamento': StringField(required=True, json_name='sequencialPagamento'),
        'valor': NumberField(required=True),
        'valor_contra_vale_ou_troco': NumberField(required=False, json_name='valorContraValeOuTroco')
    }


class PanamahTrocaDevolucaoItem(Model):
    schema = {
        'desconto': NumberField(required=False),
        'produto_id': StringField(required=True, json_name='produtoId'),
        'quantidade': NumberField(required=True),
        'valor_total': NumberField(required=True, json_name='valorTotal'),
        'valor_unitario': NumberField(required=True, json_name='valorUnitario'),
        'vendedor_id': StringField(required=False, json_name='vendedorId')
    }


class PanamahTrocaDevolucao(Model):
    name = 'TROCA_DEVOLUCAO'
    schema = {
        'autorizador_id': StringField(required=False, json_name='autorizadorId'),
        'data': DateField(required=True),
        'venda_id': StringField(required=False, json_name='vendaId'),
        'id': StringField(required=True),
        'itens': ObjectListField(required=True, object_class=PanamahTrocaDevolucaoItem),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'numero_caixa': StringField(required=False, json_name='numeroCaixa'),
        'operador_id': StringField(required=False, json_name='operadorId'),
        'sequencial': StringField(required=False),
        'valor': NumberField(required=True),
        'vendedor_id': StringField(required=False, json_name='vendedorId')
    }


class PanamahEventoCaixaValoresDeclarados(Model):
    schema = {
        'forma_pagamento_id': StringField(required=True, json_name='formaPagamentoId'),
        'valor': NumberField(required=True)
    }


class PanamahEventoCaixa(Model):
    name = 'EVENTO_CAIXA'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'numero_caixa': StringField(required=True, json_name='numeroCaixa'),
        'funcionario_id': StringField(required=False, json_name='funcionarioId'),
        'data_hora': DateField(required=True, json_name='dataHora'),
        'tipo': StringField(required=True, allowedValues=['ABERTURA', 'FECHAMENTO', 'ENTRADA_OPERADOR', 'SAIDA_OPERADOR']),
        'valores_declarados': ObjectListField(required=False, object_class=PanamahEventoCaixaValoresDeclarados, json_name='valoresDeclarados')
    }


class PanamahVendaPagamento(Model):
    schema = {
        'forma_pagamento_id': StringField(required=True, json_name='formaPagamentoId'),
        'sequencial': StringField(required=True),
        'valor': NumberField(required=True)
    }


class PanamahVendaItem(Model):
    schema = {
        'acrescimo': NumberField(required=False),
        'desconto': NumberField(required=False),
        'efetivo': BooleanField(required=True, default=True),
        'funcionario_id': StringField(required=False, json_name='funcionarioId'),
        'preco': NumberField(required=True),
        'produto_id': StringField(required=True, json_name='produtoId'),
        'codigo_registrado': StringField(required=False, json_name='codigoRegistrado'),
        'promocao': BooleanField(required=False),
        'quantidade': NumberField(required=True),
        'servico': NumberField(required=False),
        'valor_total': NumberField(required=True, json_name='valorTotal'),
        'valor_unitario': NumberField(required=True, json_name='valorUnitario'),
        'tipo_preco': StringField(required=True, json_name='tipoPreco'),
        'custo': NumberField(required=False),
        'markup': NumberField(required=False),
        'lucro': NumberField(required=False)
    }


class PanamahVenda(Model):
    name = 'VENDA'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'cliente_id': StringField(required=False, json_name='clienteId'),
        'funcionario_id': StringField(required=False, json_name='funcionarioId'),
        'data': DateField(required=True),
        'data_hora_inicio': DateField(required=False, json_name='dataHoraInicio'),
        'data_hora_fim': DateField(required=False, json_name='dataHoraFim'),
        'data_hora_venda': DateField(required=True, json_name='dataHoraVenda'),
        'desconto': NumberField(required=False),
        'efetiva': BooleanField(required=True, default=True),
        'quantidade_itens': NumberField(required=True, json_name='quantidadeItens'),
        'quantidade_itens_cancelados': NumberField(required=False),
        'sequencial': StringField(required=True),
        'servico': NumberField(required=False),
        'tipo_desconto': StringField(required=False, json_name='tipoDesconto'),
        'tipo_preco': StringField(required=True, json_name='tipoPreco'),
        'valor': NumberField(required=True),
        'valor_itens_cancelados': NumberField(required=False),
        'acrescimo': NumberField(required=False),
        'numero_caixa': StringField(required=False, json_name='numeroCaixa'),
        'itens': ObjectListField(required=True, object_class=PanamahVendaItem),
        'pagamentos': ObjectListField(required=True, object_class=PanamahVendaPagamento)
    }


class PanamahCompraItem(Model):
    schema = {
        'acrescimo': NumberField(required=False),
        'desconto': NumberField(required=False),
        'produto_id': StringField(required=True, json_name='produtoId'),
        'quantidade': NumberField(required=True),
        'valor_total': NumberField(required=True, json_name='valorTotal'),
        'valor_unitario': NumberField(required=True, json_name='valorUnitario')
    }


class PanamahCompra(Model):
    name = 'COMPRA'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'fornecedor_id': StringField(required=False, json_name='fornecedorId'),
        'funcionario_id': StringField(required=False, json_name='funcionarioId'),
        'data_entrada': DateField(required=True, json_name='dataEntrada'),
        'data_emissao': DateField(required=True, json_name='dataEmissao'),
        'data_hora_compra': DateField(required=True, json_name='dataHoraCompra'),
        'desconto': NumberField(required=False),
        'efetiva': BooleanField(required=True, default=True),
        'quantidade_itens': NumberField(required=True, json_name='quantidadeItens'),
        'tipo_desconto': StringField(required=False, json_name='tipoDesconto'),
        'valor': NumberField(required=True),
        'acrescimo': NumberField(required=False),
        'itens': ObjectListField(required=True, object_class=PanamahCompraItem)
    }


class PanamahLocalEstoque(Model):
    name = 'LOCAL_ESTOQUE'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'descricao': StringField(required=True),
        'disponivel_para_venda': BooleanField(required=True, json_name='disponivelParaVenda')
    }


class PanamahEstoqueMovimentacao(Model):
    name = 'ESTOQUE_MOVIMENTACAO'
    schema = {
        'id': StringField(required=True),
        'local_estoque_id': StringField(required=True),
        'data_hora': DateField(required=True, json_name='dataHora'),
        'produto_id': StringField(required=True, json_name='produtoId'),
        'quantidade': NumberField(required=True),
        'custo': NumberField(required=True),
        'preco': NumberField(required=True),
        'markup': NumberField(required=False)
    }


class PanamahTituloPagarPagamento(Model):
    schema = {
        'data_hora': DateField(required=True, json_name='dataHora'),
        'valor': NumberField(required=True)
    }


class PanamahTituloPagar(Model):
    name = 'TITULO_PAGAR'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'fornecedor_id': StringField(required=True, json_name='fornecedorId'),
        'documento': StringField(required=True),
        'valor_nominal': NumberField(required=True, json_name='valorNominal'),
        'valor_juros': NumberField(required=True, json_name='valorJuros'),
        'valor_multa': NumberField(required=True, json_name='valorMulta'),
        'valor_devido': NumberField(required=True, json_name='valorDevido'),
        'valor_pago': NumberField(required=True, json_name='valorPago'),
        'data_emissao': DateField(required=True, json_name='dataEmissao'),
        'data_vencimento': DateField(required=True, json_name='dataVencimento'),
        'pagamentos': ObjectListField(required=True, object_class=PanamahTituloPagarPagamento)
    }


class PanamahTituloReceberPagamento(Model):
    schema = {
        'data_hora': DateField(required=True, json_name='dataHora'),
        'valor': NumberField(required=True)
    }


class PanamahTituloReceber(Model):
    name = 'TITULO_RECEBER'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True, json_name='lojaId'),
        'cliente_id': StringField(required=True, json_name='clienteId'),
        'documento': StringField(required=True),
        'valor_nominal': NumberField(required=True, json_name='valorNominal'),
        'valor_juros': NumberField(required=True, json_name='valorJuros'),
        'valor_multa': NumberField(required=True, json_name='valorMulta'),
        'valor_devido': NumberField(required=True, json_name='valorDevido'),
        'valor_pago': NumberField(required=True, json_name='valorPago'),
        'data_emissao': DateField(required=True, json_name='dataEmissao'),
        'data_vencimento': DateField(required=True, json_name='dataVencimento'),
        'pagamentos': ObjectListField(required=True, object_class=PanamahTituloReceberPagamento)
    }


def from_json(name, json):
    for cls_name in globals():
        cls = globals()[cls_name]
        if type(cls) is type(object) and issubclass(cls, Model) and hasattr(cls, 'name') and cls.name == name:
            return cls.from_json(json)
    return None
