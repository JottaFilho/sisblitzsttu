import json
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

@st.cache_resource
def conectar():
    creds_dict = None

    # Opção 1: Tenta ler o JSON completo colado como string
    if "GOOGLE_CREDENTIALS_JSON" in st.secrets:
        try:
            raw_val = st.secrets["GOOGLE_CREDENTIALS_JSON"]
            creds_dict = json.loads(raw_val)
        except Exception as e:
            st.error(f"Erro ao converter GOOGLE_CREDENTIALS_JSON para JSON: {e}")

    # Opção 2: Tenta ler a estrutura padrão de sub-chaves do st.secrets
    elif "gspread_credentials" in st.secrets:
        creds_dict = dict(st.secrets["gspread_credentials"])

    # Se conseguiu carregar os dados de alguma das formas acima via Secrets:
    if creds_dict:
        if "private_key" in creds_dict:
            pk = creds_dict["private_key"]
            # Normaliza a chave privada para garantir quebras de linha corretas
            pk = pk.replace("\\n", "\n").strip('"').strip("'")
            creds_dict["private_key"] = pk

        credentials = Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )
    else:
        # Fallback local apenas para desenvolvimento na sua máquina
        try:
            credentials = Credentials.from_service_account_file(
                "credenciais.json",
                scopes=SCOPES
            )
        except Exception:
            raise FileNotFoundError(
                "Nenhum segredo 'GOOGLE_CREDENTIALS_JSON' foi encontrado no Streamlit Cloud "
                "e o arquivo físico 'credenciais.json' não existe na pasta."
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