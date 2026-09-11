import streamlit as st
from database.google_sheets import (
    listar_operacoes,
    criar_operacao,
    atualizar_operacao,
    excluir_operacao,
    listar_tipificacoes,
    listar_operacao_tipificacoes,
    criar_operacao_tipificacoes_lote
)

# =========================================================
# OPERAÇÕES
# =========================================================

@st.cache_data(ttl=600)
def obter_operacoes(spreadsheet_id):
    # A função list() impede que os dados se esgotem no cache
    resultados = listar_operacoes(spreadsheet_id)
    return list(resultados) if resultados else []

def cadastrar_operacao(
    spreadsheet_id,
    data,
    hora_inicio,
    hora_fim,
    local,
    sentido,
    efetivo_sttu,
    efetivo_cpre,
    veiculos_abordados,
    veiculos_removidos
):

    # -----------------------------------------------------
    # BUSCAR OPERAÇÕES EXISTENTES
    # -----------------------------------------------------
    operacoes = obter_operacoes(spreadsheet_id)

    # -----------------------------------------------------
    # GERAR NOVO ID
    # -----------------------------------------------------
    if operacoes:
        ultimo_id = max(int(operacao["id"]) for operacao in operacoes)
        novo_id = ultimo_id + 1
    else:
        novo_id = 1

    # -----------------------------------------------------
    # PREPARAR DADOS E GRAVAR
    # -----------------------------------------------------
    dados = [
        novo_id, data, hora_inicio, hora_fim, local, sentido,
        efetivo_sttu, efetivo_cpre, veiculos_abordados, veiculos_removidos
    ]

    criar_operacao(spreadsheet_id, dados)
    
    # Limpa o cache após um novo cadastro
    st.cache_data.clear()

    return novo_id


# =========================================================
# TIPIFICAÇÕES
# =========================================================

@st.cache_data(ttl=3600)
def obter_tipificacoes(spreadsheet_id):
    resultados = listar_tipificacoes(spreadsheet_id)
    return list(resultados) if resultados else []


# =========================================================
# RELACIONAMENTO
# =========================================================

@st.cache_data(ttl=600)
def obter_todas_operacao_tipificacoes(spreadsheet_id):
    resultados = listar_operacao_tipificacoes(spreadsheet_id)
    return list(resultados) if resultados else []

def cadastrar_tipificacoes_operacao(
    spreadsheet_id,
    operacao_id,
    tipificacoes
):
    if not tipificacoes:
        return

    relacionamentos = obter_todas_operacao_tipificacoes(spreadsheet_id)

    if relacionamentos:
        ultimo_id = max(int(item["id"]) for item in relacionamentos)
        proximo_id = ultimo_id + 1
    else:
        proximo_id = 1

    registros = []
    for tipificacao in tipificacoes:
        registros.append([
            proximo_id,
            operacao_id,
            tipificacao["id"],
            tipificacao["quantidade"]
        ])
        proximo_id += 1

    criar_operacao_tipificacoes_lote(spreadsheet_id, registros)
    st.cache_data.clear()


# =========================================================
# DETALHES DA OPERAÇÃO
# =========================================================

def obter_detalhes_operacao(
    spreadsheet_id,
    operacao_id
):
    # -----------------------------------------------------
    # CARREGAR DADOS COM CACHE
    # -----------------------------------------------------
    operacoes = obter_operacoes(spreadsheet_id)
    tipificacoes = obter_tipificacoes(spreadsheet_id)
    relacionamentos = obter_todas_operacao_tipificacoes(spreadsheet_id)

    # -----------------------------------------------------
    # LOCALIZAR OPERAÇÃO
    # -----------------------------------------------------
    operacao = next(
        (item for item in operacoes if int(item["id"]) == int(operacao_id)),
        None
    )

    if operacao is None:
        return None, []

    # -----------------------------------------------------
    # CRIAR MAPA DE TIPIFICAÇÕES E MONTAR DETALHES
    # -----------------------------------------------------
    mapa_tipificacoes = {int(item["id"]): item for item in tipificacoes}
    detalhes_tipificacoes = []

    for relacionamento in relacionamentos:
        if int(relacionamento["operacao_id"]) != int(operacao_id):
            continue

        tipificacao_id = int(relacionamento["tipificacao_id"])
        tipificacao = mapa_tipificacoes.get(tipificacao_id)

        if tipificacao is None:
            continue

        detalhes_tipificacoes.append({
            "codigo": tipificacao["codigo"],
            "descricao": tipificacao["descricao"],
            "quantidade": int(relacionamento["quantidade"])
        })

    return operacao, detalhes_tipificacoes

# =========================================================
# EDIÇÃO E EXCLUSÃO DE OPERAÇÕES
# =========================================================

def editar_operacao(
    spreadsheet_id,
    operacao_id,
    data,
    hora_inicio,
    hora_fim,
    local,
    sentido,
    efetivo_sttu,
    efetivo_cpre,
    veiculos_abordados,
    veiculos_removidos
):
    dados = [
        int(operacao_id),
        data,
        hora_inicio,
        hora_fim,
        local,
        sentido,
        efetivo_sttu,
        efetivo_cpre,
        veiculos_abordados,
        veiculos_removidos
    ]
    
    atualizar_operacao(
        spreadsheet_id,
        operacao_id,
        dados
    )
    
    st.cache_data.clear()


def remover_operacao(
    spreadsheet_id,
    operacao_id
):
    excluir_operacao(
        spreadsheet_id,
        operacao_id
    )
    
    st.cache_data.clear()