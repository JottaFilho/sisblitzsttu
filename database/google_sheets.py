import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# =========================================================
# CONEXÃO
# =========================================================

@st.cache_resource
def conectar():
    if "gspread_credentials" in st.secrets:
        creds_dict = dict(st.secrets["gspread_credentials"])
        
        if "private_key" in creds_dict:
            pk = creds_dict["private_key"]
            # Remove eventuais aspas duplas extras que o Streamlit ou o usuário possam ter colocado
            pk = pk.strip('"').strip("'")
            
            # Se a chave foi colada sem quebras reais ou com \n literal, normaliza para o formato PEM
            if "-----BEGIN PRIVATE KEY-----" in pk and "-----END PRIVATE KEY-----" in pk:
                # Se não tem quebras reais, reconstrói o formato correto
                if "\n" not in pk.replace("\\n", "\n"):
                    # Remove os headers e footers para limpar o miolo
                    body = pk.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
                    body = "".join(body.split()) # Remove espaços e quebras falsas
                    # Reorganiza em blocos de 64 caracteres (padrão PEM)
                    formatted_body = "\n".join(body[i:i+64] for i in range(0, len(body), 64))
                    pk = f"-----BEGIN PRIVATE KEY-----\n{formatted_body}\n-----END PRIVATE KEY-----\n"
                else:
                    pk = pk.replace("\\n", "\n")
            
            creds_dict["private_key"] = pk

        credentials = Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )
    else:
        credentials = Credentials.from_service_account_file(
            "credenciais.json",
            scopes=SCOPES
        )

    return gspread.authorize(credentials)



@st.cache_resource
def obter_planilha(spreadsheet_id):

    client = conectar()

    return client.open_by_key(
        spreadsheet_id
    )


def obter_aba(
    spreadsheet_id,
    nome_aba
):

    spreadsheet = obter_planilha(
        spreadsheet_id
    )

    return spreadsheet.worksheet(
        nome_aba
    )


# =========================================================
# OPERAÇÕES
# =========================================================

@st.cache_data(ttl=30)
def listar_operacoes(spreadsheet_id):

    worksheet = obter_aba(
        spreadsheet_id,
        "operacoes"
    )

    return worksheet.get_all_records()


def criar_operacao(
    spreadsheet_id,
    dados
):

    worksheet = obter_aba(
        spreadsheet_id,
        "operacoes"
    )

    worksheet.append_row(
        dados,
        value_input_option="USER_ENTERED"
    )

    # Limpa o cache para a próxima leitura
    listar_operacoes.clear()


def atualizar_operacao(
    spreadsheet_id,
    operacao_id,
    dados
):
    worksheet = obter_aba(
        spreadsheet_id,
        "operacoes"
    )

    # Localiza a linha com base no ID da operação (coluna 1)
    celula = worksheet.find(str(operacao_id))
    
    if celula:
        linha = celula.row
        # Monta o intervalo da linha (coluna A até J, por exemplo)
        # Como temos 10 colunas, atualizamos a linha inteira de uma vez
        worksheet.update(f"A{linha}:J{linha}", [dados], value_input_option="USER_ENTERED")
        listar_operacoes.clear()


def excluir_operacao(
    spreadsheet_id,
    operacao_id
):
    worksheet_op = obter_aba(
        spreadsheet_id,
        "operacoes"
    )
    
    celula = worksheet_op.find(str(operacao_id))
    if celula:
        worksheet_op.delete_rows(celula.row)
        listar_operacoes.clear()

    # Também remove os relacionamentos de tipificações desta operação
    worksheet_tip = obter_aba(
        spreadsheet_id,
        "operacao_tipificacoes"
    )
    
    # Busca todas as linhas de relacionamento para apagar as que pertencem a este ID
    try:
        celulas = worksheet_tip.findall(str(operacao_id))
        # Apaga de trás para frente para não alterar os índices das linhas restantes
        linhas_para_apagar = sorted([c.row for c in celulas], reverse=True)
        for linha in linhas_para_apagar:
            worksheet_tip.delete_rows(linha)
            
        listar_operacao_tipificacoes.clear()
    except Exception:
        pass


# =========================================================
# TIPIFICAÇÕES
# =========================================================

@st.cache_data(ttl=300)
def listar_tipificacoes(spreadsheet_id):

    worksheet = obter_aba(
        spreadsheet_id,
        "tipificacoes"
    )

    return worksheet.get_all_records()


# =========================================================
# RELACIONAMENTOS
# =========================================================

@st.cache_data(ttl=30)
def listar_operacao_tipificacoes(
    spreadsheet_id
):

    worksheet = obter_aba(
        spreadsheet_id,
        "operacao_tipificacoes"
    )

    return worksheet.get_all_records()


def criar_operacao_tipificacoes_lote(
    spreadsheet_id,
    dados
):

    if not dados:
        return

    worksheet = obter_aba(
        spreadsheet_id,
        "operacao_tipificacoes"
    )

    worksheet.append_rows(
        dados,
        value_input_option="USER_ENTERED"
    )

    # Limpa o cache
    listar_operacao_tipificacoes.clear()