# coding: utf-8

RESOURCE_MAPPING = {
    "clients": {
        "resource": "financeiro/clientes",
        "methods": ["GET", "POST", "PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes",
    },
    "edit_client_contact": {
        "resource": "financeiro/contatos",
        "methods": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/cadastro-consulta-e-edicao/editar-um-contato-do-cliente?console=1",
    },
    "remove_client_contact": {
        "resource": "financeiro/contatos/delete",
        "methods": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/cadastro-consulta-e-edicao/remover-um-contato-do-cliente?console=1",
    },
    "create_acess_token": {
        "resource": "financeiro/clientes/token",
        "methods": ["POST"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/cadastro-consulta-e-edicao/gerar-token-de-acesso-do-cliente?console=1",
    },
    "defrayers": {
        "resource": "financeiro/clientes/adimplentes",
        "methods": ["GET"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/cadastro-consulta-e-edicao/obter-clientes-adimplentes?console=1",
    },
    "defaulters": {
        "resource": "financeiro/clientes/inadimplencia",
        "methods": ["GET"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/cadastro-consulta-e-edicao/obter-clientes-inadimplentes?console=1",
    },
    "url_change_credicard": {
        "resource": "financeiro/clientes/urlcartao",
        "methods": ["GET"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/cadastro-consulta-e-edicao/consultar-url-para-troca-de-cartao?console=1",
    },
    "payment_overdue": {
        "resource": "financeiro/inadimplencia",
        "methods": ["GET"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/inadimplencia/consultar/consultar-inadimplencia?console=1",
    },
    "group_client": {
        "resource": "financeiro/grupo/clientes",
        "methods": ["GET", "POST", "PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/grupos-de-clientes/criar-um-novo-grupo-de-clientes?console=1",
    },
    "remove_client_from_group": {
        "resource": "financeiro/cliente/desagrupar",
        "methods": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/clientes/grupos-de-clientes/excluir-cliente-de-um-grupo?console=1",
    },
    "signatures": {
        "resource": "financeiro/assinaturas",
        "methods": ["GET", "POST", "PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/assinaturas",
    },
    "migrate_signatures": {
        "resource": "financeiros/assinaturas/migrar",
        "methods": ["GET", "POST", "PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/assinaturas/contratacao-consulta-e-cancelamento/migrar-um-plano?console=1",
    },
    "trial_contracts": {
        "resource": "financeiro/recorrencias/recorrenciasdeplanos",
        "methods": ["GET"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/assinaturas/contratacao-consulta-e-cancelamento/consultar-contratos-em-trial?console=1",
    },
    "change_seller_signature": {
        "resource": "financeiro/assinaturas/alterarvendedor",
        "methdos": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/assinaturas/contratacao-consulta-e-cancelamento/alterar-vendedor-de-uma-assinatura?console=1",
    },
    "change_item_signature": {
        "methods": "financeiro/recorrencias",
        "methods": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/assinaturas/contratacao-consulta-e-cancelamento/alterar-item-da-assinatura?console=1",
    },
    "change_payment_methods": {
        "resource": "financeiro/clientes/formadepagamento",
        "methdos": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/assinaturas/alterar-formas-de-pagamento/alterar-forma-de-pagamento-sem-token-do-cartao?console=1",
    },
    "charges": {
        "resource": "financeiro/cobranca",
        "methods": ["GET", "POST", "PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/cobrancas/cadastro-consulta-e-edicao/listar-todas-as-cobrancas?console=1",
    },
    "settle_charge": {
        "resource": "financeiro/cobranca/liquidar",
        "methods": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/assinaturas/alterar-formas-de-pagamento/liquidar-uma-cobranca?console=1",
    },
    "reverse_charge": {
        "resource": "financeiro/cobranca/estornar",
        "methods": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/cobrancas/cadastro-consulta-e-edicao/estornar-uma-cobranca?console=1",
    },
    "cancel_credicard_payment": {
        "resource": "financeiro/cobranca/cancelarcielo",
        "methods": ["PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/cobrancas/cadastro-consulta-e-edicao/cancelar-pagamento-no-cartao-de-credito?console=1",
    },
    "group_clients": {
        "resource": "financeiro/grupoclientes",
        "methods": ["GET", "POST", "PUT"],
        "docs": "url",
    },
    "plan": {
        "resource": "financeiro/planos",
        "methods": ["GET", "POST", "PUT"],
        "docs": "https://superlogicaassinaturas.docs.apiary.io/#reference/planos/cadastrar-editar-consultar",
    },
    "product": {
        "resource": "financeiro/produtos",
        "methods": ["GET", "POST", "PUT"],
        "url": "https://superlogicaassinaturas.docs.apiary.io/#reference/produtos-e-servicos/cadastrar-editar-consultar",
    },
    "monthly_payment": {
        "resource": "financeiro/recorrencias",
        "methods": ["GET", "POST"],
        "url": "https://superlogicaassinaturas.docs.apiary.io/#reference/mensalidade/cadastro/consultar-recorrencia-de-um-cliente?console=1",
    },
}
