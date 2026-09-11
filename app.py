import streamlit as st
import pandas as pd
import plotly.express as px

from services.operacoes import (
    obter_operacoes,
    cadastrar_operacao,
    obter_tipificacoes,
    cadastrar_tipificacoes_operacao,
    obter_detalhes_operacao,
    obter_todas_operacao_tipificacoes,
    editar_operacao,
    remover_operacao
)


# =========================================================
# CONFIGURAÇÃO
# =========================================================

SPREADSHEET_ID = "1NqFjgNXslxO3dQVRxx0vZomRFQ1Y68ECmoN6BbRVI2Y"


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Cadastro de Blitz",
    page_icon="🚦",
    layout="wide"
)


# =========================================================
# ESTILO CUSTOMIZADO (MODERN UI / CARDS)
# =========================================================

st.markdown("""
    <style>
    /* 1. Fundo de toda a aplicação */
    .stApp {
        background-color: #F4F7FC;
    }
    
    /* 2. Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #FAFAFB !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* 3. BOTÕES DO MENU (SIDEBAR) - ESTILO CARD EM AZUL CLARO */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #93C5FD !important; 
        color: #1E3A8A !important;          
        border: none !important;
        text-align: center !important;
        justify-content: center !important;
        padding: 0.7rem 1rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }
    
    /* Efeito ao passar o mouse (Hover) -> Azul mais escuro */
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #2563EB !important; 
        color: white !important;
        box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.25) !important;
    }
    
    /* Botão da página ATIVA (Selecionada) -> Azul mais escuro */
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #1D4ED8 !important; 
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0px 4px 12px rgba(29, 78, 216, 0.3) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background-color: #1E40AF !important;
    }

    /* 4. Estilização das Métricas (Cards modernos do corpo) */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 15px 25px;
        box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid #E9ECEF;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 5px;
    }

    [data-testid="stMetricValue"] {
        color: #1E293B !important;
        font-size: 32px !important;
        font-weight: 800 !important;
    }

    /* 5. Inputs e Filtros */
    .stSelectbox div[data-baseweb="select"] > div, 
    .stDateInput > div {
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
    }

    /* 6. Botões gerais do corpo da aplicação */
    .stButton > button {
        border-radius: 12px !important;
        background-color: #3B82F6 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #2563EB !important;
        box-shadow: 0px 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
        border-color: #E2E8F0;
    }

    .page-header {
        background: linear-gradient(90deg, #60A5FA 0%, #3B82F6 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        margin-bottom: 2rem;
        color: white;
    }

    .page-header h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
    }

    .page-header p {
        margin: 0.3rem 0 0 0;
        font-size: 1rem;
        color: white;
        opacity: 0.95;
    }
    </style>
""", unsafe_allow_html=True)


# =========================================================
# COMPONENTE: CABEÇALHO DAS PÁGINAS
# =========================================================

def cabecalho_pagina(icone, titulo, descricao):
    st.markdown(
        f"""
        <div class="page-header">
            <h2>{icone} {titulo}</h2>
            <p>{descricao}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TÍTULO PRINCIPAL
# =========================================================

st.markdown("""
    <div style="margin-top: -1rem; margin-bottom: 2rem;">
        <h1 style="color: #0F172A; font-size: 2.8rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 0rem;">
            Cadastro de Blitz
        </h1>
        <p style="color: #64748B; font-size: 1.1rem; font-weight: 500; margin-top: 0.2rem;">
            Secretaria Municipal de Trânsito e Mobilidade Urbana — STTU / SEAT
        </p>
    </div>
""", unsafe_allow_html=True)


# =========================================================
# ESTADO DA NAVEGAÇÃO
# =========================================================

if "operacao_selecionada" not in st.session_state:
    st.session_state.operacao_selecionada = None


# =========================================================
# MENU / SIDEBAR
# =========================================================

paginas = [
    "📊 Dashboard",
    "📋 Operações",
    "➕ Nova Operação",
    "🔎 Detalhes da Operação",
]

if "pagina" not in st.session_state:
    st.session_state.pagina = "📊 Dashboard"

with st.sidebar:
    # Cria 3 colunas para centralizar a do meio
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.image("logo_sttu.png", width=100)
    
    st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
    
    for pagina in paginas:
        is_ativo = st.session_state.pagina == pagina
        
        if st.button(pagina, use_container_width=True, key=f"nav_{pagina}"):
            st.session_state.pagina = pagina
            st.rerun()

opcao = st.session_state.pagina


# =========================================================
# DASHBOARD
# =========================================================

if opcao == "📊 Dashboard":

    cabecalho_pagina(
        "📊",
        "Dashboard Gerencial",
        "Visão consolidada das operações e indicadores de fiscalização"
    )

    operacoes = obter_operacoes(SPREADSHEET_ID)

    if not operacoes:
        st.info("Nenhuma operação cadastrada para gerar o dashboard.")
    else:
        st.subheader("🔎 Filtros")

        col1, col2, col3 = st.columns(3)

        with col1:
            data_inicial = st.date_input("Data inicial", value=None, key="dashboard_data_inicial")

        with col2:
            data_final = st.date_input("Data final", value=None, key="dashboard_data_final")

        with col3:
            locais = sorted(set(op["local"] for op in operacoes if op["local"]))
            local_filtro = st.selectbox("Local", options=["Todos"] + locais, key="dashboard_local")

        operacoes_filtradas = []
        for operacao in operacoes:
            incluir = True
            data_operacao = operacao["data"]

            if data_inicial and data_operacao < data_inicial.strftime("%Y-%m-%d"):
                incluir = False
            if data_final and data_operacao > data_final.strftime("%Y-%m-%d"):
                incluir = False
            if local_filtro != "Todos" and operacao["local"] != local_filtro:
                incluir = False

            if incluir:
                operacoes_filtradas.append(operacao)

        total_operacoes = len(operacoes_filtradas)
        total_abordados = sum(int(op["veiculos_abordados"]) for op in operacoes_filtradas)
        total_removidos = sum(int(op["veiculos_removidos"]) for op in operacoes_filtradas)
        total_sttu = sum(int(op["efetivo_sttu"]) for op in operacoes_filtradas)
        total_cpre = sum(int(op["efetivo_cpre"]) for op in operacoes_filtradas)

        taxa_remocao = (total_removidos / total_abordados * 100) if total_abordados > 0 else 0

        st.divider()
        st.subheader("📊 Indicadores gerais")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🚦 Operações", total_operacoes)
        with col2:
            st.metric("🚗 Veículos abordados", total_abordados)
        with col3:
            st.metric("🚨 Veículos removidos", total_removidos)
        with col4:
            st.metric("📈 Taxa de remoção", f"{taxa_remocao:.1f}%")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("👮 Efetivo STTU", total_sttu)
        with col2:
            st.metric("👮 Efetivo CPRE", total_cpre)

        if not operacoes_filtradas:
            st.warning("Nenhuma operação encontrada com os filtros selecionados.")
        else:
            st.divider()
            st.subheader("📅 Operações por período")

            operacoes_por_data = {}
            for op in operacoes_filtradas:
                data = op["data"]
                operacoes_por_data[data] = operacoes_por_data.get(data, 0) + 1

            df_periodo = pd.DataFrame({
                "Data": list(operacoes_por_data.keys()),
                "Operações": list(operacoes_por_data.values())
            })

            fig_periodo = px.line(df_periodo, x="Data", y="Operações", markers=True, text="Operações")
            fig_periodo.update_traces(textposition="top center")
            fig_periodo.update_layout(xaxis_title="Data", yaxis_title="Quantidade de operações", height=400)
            st.plotly_chart(fig_periodo, use_container_width=True)

            st.subheader("🚗 Veículos abordados x removidos")
            df_veiculos = pd.DataFrame({
                "Categoria": ["Abordados", "Removidos"],
                "Quantidade": [total_abordados, total_removidos]
            })
            fig_veiculos = px.bar(df_veiculos, x="Categoria", y="Quantidade", text="Quantidade", color="Categoria", color_discrete_sequence=["#3b82f6", "#ef4444"])
            fig_veiculos.update_traces(textposition="outside")
            fig_veiculos.update_layout(xaxis_title="", yaxis_title="Quantidade de veículos", showlegend=False, height=400)
            st.plotly_chart(fig_veiculos, use_container_width=True)

            st.subheader("📍 Operações por local")
            operacoes_por_local = {}
            for op in operacoes_filtradas:
                local = op["local"]
                operacoes_por_local[local] = operacoes_por_local.get(local, 0) + 1

            df_local = pd.DataFrame({
                "Local": list(operacoes_por_local.keys()),
                "Operações": list(operacoes_por_local.values())
            }).sort_values("Operações", ascending=True)

            fig_local = px.bar(df_local, x="Operações", y="Local", orientation="h", text="Operações")
            fig_local.update_traces(textposition="outside")
            fig_local.update_layout(xaxis_title="Quantidade de operações", yaxis_title="", height=500)
            st.plotly_chart(fig_local, use_container_width=True)

            st.divider()
            st.subheader("⚖️ Análise de Infrações")

            todas_tipificacoes = obter_tipificacoes(SPREADSHEET_ID)
            todos_relacionamentos = obter_todas_operacao_tipificacoes(SPREADSHEET_ID)

            if not todas_tipificacoes or not todos_relacionamentos:
                st.info("Não há dados de infrações suficientes para gerar os gráficos.")
            else:
                ids_operacoes_filtradas = [int(op["id"]) for op in operacoes_filtradas]
                relacionamentos_filtrados = [
                    rel for rel in todos_relacionamentos
                    if int(rel["operacao_id"]) in ids_operacoes_filtradas
                ]

                if not relacionamentos_filtrados:
                    st.warning("Nenhuma infração registrada para os filtros selecionados.")
                else:
                    mapa_tip_codigo = {int(t["id"]): t["codigo"] for t in todas_tipificacoes}
                    contagem_infracoes = {}

                    for rel in relacionamentos_filtrados:
                        tip_id = int(rel["tipificacao_id"])
                        qtd = int(rel["quantidade"])
                        codigo_infracao = mapa_tip_codigo.get(tip_id, f"ID {tip_id}")
                        contagem_infracoes[codigo_infracao] = contagem_infracoes.get(codigo_infracao, 0) + qtd

                    df_infracoes = pd.DataFrame({
                        "Infração": list(contagem_infracoes.keys()),
                        "Quantidade": list(contagem_infracoes.values())
                    }).sort_values("Quantidade", ascending=True)

                    fig_infracoes = px.bar(df_infracoes, x="Quantidade", y="Infração", orientation="h", title="Ranking das Infrações Mais Constatadas", text="Quantidade")
                    fig_infracoes.update_traces(textposition="outside")
                    fig_infracoes.update_layout(xaxis_title="Quantidade de registros", yaxis_title="", height=500)
                    st.plotly_chart(fig_infracoes, use_container_width=True)

                    st.divider()
                    st.subheader("📍 Tipificações Específicas por Local")

                    mapa_op_local = {int(op["id"]): op["local"] for op in operacoes_filtradas}
                    dados_tip_local = []
                    for rel in relacionamentos_filtrados:
                        op_id = int(rel["operacao_id"])
                        local = mapa_op_local.get(op_id)
                        if local:
                            tip_id = int(rel["tipificacao_id"])
                            codigo = mapa_tip_codigo.get(tip_id, f"ID {tip_id}")
                            qtd = int(rel["quantidade"])
                            dados_tip_local.append({"Local": local, "Infração": codigo, "Quantidade": qtd})

                    if dados_tip_local:
                        df_tip_local = pd.DataFrame(dados_tip_local)
                        df_tip_local = df_tip_local.groupby(["Infração", "Local"], as_index=False)["Quantidade"].sum()

                        infracoes_disponiveis = sorted(df_tip_local["Infração"].unique())
                        opcoes_filtro = ["Todas as Infrações"] + infracoes_disponiveis

                        infracao_selecionada = st.selectbox(
                            "Selecione a infração para analisar o mapa de calor por via:",
                            options=opcoes_filtro,
                            key="select_infracao_local"
                        )

                        if infracao_selecionada == "Todas as Infrações":
                            df_plot = df_tip_local.groupby("Local", as_index=False)["Quantidade"].sum().sort_values(by="Quantidade", ascending=True)
                            titulo_grafico = "Total de Infrações por Local (Visão Geral)"
                        else:
                            df_plot = df_tip_local[df_tip_local["Infração"] == infracao_selecionada].sort_values(by="Quantidade", ascending=True)
                            titulo_grafico = f"Locais com maior incidência: {infracao_selecionada}"

                        fig_tip_local = px.bar(df_plot, x="Quantidade", y="Local", orientation="h", text="Quantidade")
                        fig_tip_local.update_traces(textposition="outside")
                        fig_tip_local.update_layout(xaxis_title="Quantidade de registros", yaxis_title="", title=titulo_grafico, height=400)
                        st.plotly_chart(fig_tip_local, use_container_width=True)

            st.divider()
            col_espaco, col_pdf = st.columns([2, 1])
            with col_pdf:
                from utils.pdf_generator import gerar_pdf_relatorio

                metricas_dict = {
                    "total_op": total_operacoes,
                    "abordados": total_abordados,
                    "removidos": total_removidos,
                    "sttu": total_sttu,
                    "cpre": total_cpre,
                    "taxa_remocao": f"{taxa_remocao:.1f}%"
                }

                tabela_pdf_dados = []
                for operacao in operacoes_filtradas:
                    tabela_pdf_dados.append({
                        "ID": operacao["id"],
                        "Data": operacao["data"],
                        "Local": operacao["local"],
                        "Abordados": operacao["veiculos_abordados"],
                        "Removidos": operacao["veiculos_removidos"]
                    })
                df_pdf = pd.DataFrame(tabela_pdf_dados)

                # Tenta exportar os gráficos como imagem; se o Kaleido falhar na nuvem, passa None para o PDF não quebrar
                try:
                    img_periodo_bytes = fig_periodo.to_image(format="png", width=700, height=300, scale=2)
                    img_veiculos_bytes = fig_veiculos.to_image(format="png", width=600, height=250, scale=2)
                    img_local_bytes = fig_local.to_image(format="png", width=700, height=350, scale=2)
                except Exception:
                    img_periodo_bytes = None
                    img_veiculos_bytes = None
                    img_local_bytes = None

                pdf_bytes = gerar_pdf_relatorio(
                    metricas_dict,
                    df_pdf,
                    imagem_grafico_periodo=img_periodo_bytes,
                    imagem_grafico_veiculos=img_veiculos_bytes,
                    imagem_grafico_local=img_local_bytes
                )

                st.download_button(
                    label="📄 Baixar Relatório Gerencial (PDF)",
                    data=pdf_bytes,
                    file_name="relatorio_gerencial_seat_sttu.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


# =========================================================
# OPERAÇÕES
# =========================================================

elif opcao == "📋 Operações":

    cabecalho_pagina(
        "📋",
        "Operações Cadastradas",
        "Consulte, filtre e gerencie todas as operações de fiscalização registradas"
    )

    operacoes = obter_operacoes(SPREADSHEET_ID)

    if not operacoes:
        st.info("Nenhuma operação cadastrada.")
    else:
        st.subheader("🔎 Filtros")

        col1, col2, col3 = st.columns(3)
        with col1:
            data_inicial = st.date_input("Data inicial", value=None)
        with col2:
            data_final = st.date_input("Data final", value=None)
        with col3:
            locais = sorted(set(op["local"] for op in operacoes if op["local"]))
            local_filtro = st.selectbox("Local", options=["Todos"] + locais)

        operacoes_filtradas = []
        for operacao in operacoes:
            incluir = True
            if data_inicial and operacao["data"] < data_inicial.strftime("%Y-%m-%d"):
                incluir = False
            if data_final and operacao["data"] > data_final.strftime("%Y-%m-%d"):
                incluir = False
            if local_filtro != "Todos" and operacao["local"] != local_filtro:
                incluir = False
            if incluir:
                operacoes_filtradas.append(operacao)

        st.divider()
        st.subheader("📊 Indicadores")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Operações", len(operacoes_filtradas))
        with col2:
            total_abordados = sum(int(op["veiculos_abordados"]) for op in operacoes_filtradas)
            st.metric("Veículos abordados", total_abordados)
        with col3:
            total_removidos = sum(int(op["veiculos_removidos"]) for op in operacoes_filtradas)
            st.metric("Veículos removidos", total_removidos)
        with col4:
            taxa_remocao = (total_removidos / total_abordados * 100) if total_abordados > 0 else 0
            st.metric("Taxa de remoção", f"{taxa_remocao:.1f}%")

        st.divider()
        st.subheader("📋 Resultados")

        if not operacoes_filtradas:
            st.warning("Nenhuma operação encontrada com os filtros selecionados.")
        else:
            tabela = []
            for operacao in operacoes_filtradas:
                tabela.append({
                    "ID": operacao["id"],
                    "Data": operacao["data"],
                    "Início": operacao["hora_inicio"],
                    "Fim": operacao["hora_fim"],
                    "Local": operacao["local"],
                    "Sentido": operacao["sentido"],
                    "STTU": operacao["efetivo_sttu"],
                    "CPRE": operacao["efetivo_cpre"],
                    "Abordados": operacao["veiculos_abordados"],
                    "Removidos": operacao["veiculos_removidos"]
                })

            st.dataframe(tabela, use_container_width=True, hide_index=True)

            st.divider()
            import io
            output = io.BytesIO()
            df_export = pd.DataFrame(tabela)
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_export.to_excel(writer, sheet_name='Operacoes_Filtradas', index=False)
            excel_data = output.getvalue()

            st.download_button(
                label="📥 Baixar relatório em Excel (XLSX)",
                data=excel_data,
                file_name="relatorio_operacoes_blitz.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            st.divider()
            st.subheader("🔎 Visualizar operação")

            opcoes_detalhes = {
                f"Operação #{op['id']} — {op['data']} — {op['local']}": int(op["id"])
                for op in operacoes_filtradas
            }

            if opcoes_detalhes:
                operacao_escolhida = st.selectbox("Escolha uma operação", options=list(opcoes_detalhes.keys()))
                if st.button("🔎 Ver detalhes", use_container_width=True):
                    st.session_state.operacao_selecionada = opcoes_detalhes[operacao_escolhida]
                    st.session_state.pagina = "🔎 Detalhes da Operação"
                    st.rerun()


# =========================================================
# NOVA OPERAÇÃO
# =========================================================

elif opcao == "➕ Nova Operação":

    cabecalho_pagina(
        "➕",
        "Nova Operação",
        "Cadastre uma nova operação de fiscalização preenchendo os dados abaixo"
    )

    if "etapa_operacao" not in st.session_state:
        st.session_state.etapa_operacao = 1

    if "mensagem_sucesso" in st.session_state:
        st.success(st.session_state.mensagem_sucesso)
        del st.session_state.mensagem_sucesso

    if "mensagem_tipificacoes" in st.session_state:
        st.success(st.session_state.mensagem_tipificacoes)
        del st.session_state.mensagem_tipificacoes

    tipificacoes = obter_tipificacoes(SPREADSHEET_ID)
    opcoes_tipificacoes = {
        f"{tipificacao['codigo']} — {tipificacao['descricao']}": int(tipificacao["id"])
        for tipificacao in tipificacoes
    }

    if st.session_state.etapa_operacao == 1:
        st.subheader("📋 Dados da operação")

        with st.form("form_dados_operacao"):
            col1, col2 = st.columns(2)
            with col1:
                data = st.date_input("Data")
                hora_inicio = st.time_input("Hora de início")
                local = st.text_input("Local")
                sentido = st.text_input("Sentido")
                efetivo_sttu = st.number_input("Efetivo STTU", min_value=0, step=1)
            with col2:
                hora_fim = st.time_input("Hora de fim")
                efetivo_cpre = st.number_input("Efetivo CPRE", min_value=0, step=1)
                veiculos_abordados = st.number_input("Veículos abordados", min_value=0, step=1)
                veiculos_removidos = st.number_input("Veículos removidos", min_value=0, step=1)

            st.divider()
            st.subheader("⚖️ Tipificações")
            selecionadas = st.multiselect("Selecione as tipificações constatadas", options=list(opcoes_tipificacoes.keys()))

            continuar = st.form_submit_button("➡️ Continuar", use_container_width=True)

        if continuar:
            if not local.strip():
                st.error("Informe o local da operação.")
            elif not sentido.strip():
                st.error("Informe o sentido da operação.")
            elif veiculos_removidos > veiculos_abordados:
                st.error("Veículos removidos não podem ser maiores que veículos abordados.")
            elif not selecionadas:
                st.error("Selecione pelo menos uma tipificação.")
            else:
                st.session_state.dados_operacao = {
                    "data": data.strftime("%Y-%m-%d"),
                    "hora_inicio": hora_inicio.strftime("%H:%M"),
                    "hora_fim": hora_fim.strftime("%H:%M"),
                    "local": local,
                    "sentido": sentido,
                    "efetivo_sttu": efetivo_sttu,
                    "efetivo_cpre": efetivo_cpre,
                    "veiculos_abordados": veiculos_abordados,
                    "veiculos_removidos": veiculos_removidos
                }
                st.session_state.tipificacoes_selecionadas = [opcoes_tipificacoes[item] for item in selecionadas]
                st.session_state.etapa_operacao = 2
                st.rerun()

    elif st.session_state.etapa_operacao == 2:
        st.subheader("⚖️ Quantidade das tipificações")
        st.info("Informe a quantidade constatada para cada tipificação.")

        quantidades = {}
        for tipificacao_id in st.session_state.tipificacoes_selecionadas:
            tipificacao = next(item for item in tipificacoes if int(item["id"]) == tipificacao_id)
            descricao = f"{tipificacao['codigo']} — {tipificacao['descricao']}"
            quantidade = st.number_input(descricao, min_value=1, value=1, step=1, key=f"qtd_{tipificacao_id}")
            quantidades[tipificacao_id] = quantidade

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            voltar = st.button("⬅️ Voltar", use_container_width=True)
        with col2:
            salvar = st.button("💾 Cadastrar operação", use_container_width=True)

        if voltar:
            st.session_state.etapa_operacao = 1
            st.rerun()

        if salvar:
            dados = st.session_state.dados_operacao
            novo_id = cadastrar_operacao(
                SPREADSHEET_ID, dados["data"], dados["hora_inicio"], dados["hora_fim"],
                dados["local"], dados["sentido"], dados["efetivo_sttu"], dados["efetivo_cpre"],
                dados["veiculos_abordados"], dados["veiculos_removidos"]
            )

            dados_tipificacoes = [{"id": tid, "quantidade": qtd} for tid, qtd in quantidades.items()]
            cadastrar_tipificacoes_operacao(SPREADSHEET_ID, novo_id, dados_tipificacoes)

            st.session_state.etapa_operacao = 1
            del st.session_state.dados_operacao
            del st.session_state.tipificacoes_selecionadas
            st.session_state.mensagem_sucesso = f"✅ Operação #{novo_id} cadastrada com sucesso!"
            st.session_state.mensagem_tipificacoes = f"⚖️ {len(dados_tipificacoes)} tipificação(ões) registrada(s)."
            st.rerun()


# =========================================================
# DETALHES DA OPERAÇÃO
# =========================================================

elif opcao == "🔎 Detalhes da Operação":

    cabecalho_pagina(
        "🔎",
        "Detalhes da Operação",
        "Visualize informações completas, edite ou exclua uma operação selecionada"
    )

    operacoes = obter_operacoes(SPREADSHEET_ID)

    if not operacoes:
        st.info("Nenhuma operação cadastrada.")
    else:
        if st.session_state.operacao_selecionada:
            operacao_id = st.session_state.operacao_selecionada
            operacao, detalhes_tipificacoes = obter_detalhes_operacao(SPREADSHEET_ID, operacao_id)

            if operacao is None:
                st.error("Operação não encontrada.")
                st.session_state.operacao_selecionada = None
                st.rerun()
            else:
                st.subheader(f"🚦 Operação #{operacao['id']}")

                if st.button("⬅️ Voltar para operações"):
                    st.session_state.operacao_selecionada = None
                    st.rerun()

                st.divider()
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Veículos abordados", operacao["veiculos_abordados"])
                with col2:
                    st.metric("Veículos removidos", operacao["veiculos_removidos"])
                with col3:
                    abordados = int(operacao["veiculos_abordados"])
                    removidos = int(operacao["veiculos_removidos"])
                    taxa = (removidos / abordados * 100) if abordados > 0 else 0
                    st.metric("Taxa de remoção", f"{taxa:.1f}%")
                with col4:
                    total_tipificacoes = sum(item["quantidade"] for item in detalhes_tipificacoes)
                    st.metric("Tipificações", total_tipificacoes)

                st.divider()
                st.subheader("📋 Informações da operação")

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Data:** {operacao['data']}")
                    st.write(f"**Horário:** {operacao['hora_inicio']} às {operacao['hora_fim']}")
                    st.write(f"**Local:** {operacao['local']}")
                    st.write(f"**Sentido:** {operacao['sentido']}")
                with col2:
                    st.write(f"**Efetivo STTU:** {operacao['efetivo_sttu']}")
                    st.write(f"**Efetivo CPRE:** {operacao['efetivo_cpre']}")

                st.divider()
                col_btn1, col_btn2 = st.columns(2)

                with col_btn1:
                    if st.button("✏️ Editar operação", use_container_width=True):
                        st.session_state.editando_operacao = True
                        st.rerun()

                with col_btn2:
                    if st.button("🗑️ Excluir operação", use_container_width=True, type="primary"):
                        st.session_state.confirmar_exclusao = True
                        st.rerun()

                if st.session_state.get("confirmar_exclusao", False):
                    st.warning("⚠️ Tem certeza que deseja excluir esta operação permanentemente?")
                    col_conf1, col_conf2 = st.columns(2)
                    with col_conf1:
                        if st.button("❌ Sim, excluir", use_container_width=True):
                            remover_operacao(SPREADSHEET_ID, operacao_id)
                            st.session_state.operacao_selecionada = None
                            st.session_state.confirmar_exclusao = False
                            st.success("Operação excluída com sucesso!")
                            st.rerun()
                    with col_conf2:
                        if st.button("↩️ Cancelar", use_container_width=True):
                            st.session_state.confirmar_exclusao = False
                            st.rerun()

                if st.session_state.get("editando_operacao", False):
                    st.divider()
                    st.subheader("✏️ Editando Operação")

                    with st.form("form_editar_operacao"):
                        col_ed1, col_ed2 = st.columns(2)
                        with col_ed1:
                            from datetime import datetime
                            data_atual = datetime.strptime(operacao["data"], "%Y-%m-%d").date()
                            hora_ini_atual = datetime.strptime(operacao["hora_inicio"], "%H:%M").time()

                            nova_data = st.date_input("Data", value=data_atual)
                            nova_hora_inicio = st.time_input("Hora de início", value=hora_ini_atual)
                            novo_local = st.text_input("Local", value=operacao["local"])
                            novo_sentido = st.text_input("Sentido", value=operacao["sentido"])
                            novo_sttu = st.number_input("Efetivo STTU", min_value=0, value=int(operacao["efetivo_sttu"]), step=1)
                        with col_ed2:
                            hora_fim_atual = datetime.strptime(operacao["hora_fim"], "%H:%M").time()
                            nova_hora_fim = st.time_input("Hora de fim", value=hora_fim_atual)
                            novo_cpre = st.number_input("Efetivo CPRE", min_value=0, value=int(operacao["efetivo_cpre"]), step=1)
                            novos_abordados = st.number_input("Veículos abordados", min_value=0, value=int(operacao["veiculos_abordados"]), step=1)
                            novos_removidos = st.number_input("Veículos removidos", min_value=0, value=int(operacao["veiculos_removidos"]), step=1)

                        col_salvar, col_cancelar = st.columns(2)
                        with col_salvar:
                            salvar_edicao = st.form_submit_button("💾 Salvar alterações", use_container_width=True)
                        with col_cancelar:
                            cancelar_edicao = st.form_submit_button("❌ Cancelar", use_container_width=True)

                        if salvar_edicao:
                            if not novo_local.strip():
                                st.error("O local não pode estar vazio.")
                            elif novos_removidos > novos_abordados:
                                st.error("Veículos removidos não podem ser maiores que os abordados.")
                            else:
                                editar_operacao(
                                    SPREADSHEET_ID, operacao_id,
                                    nova_data.strftime("%Y-%m-%d"), nova_hora_inicio.strftime("%H:%M"),
                                    nova_hora_fim.strftime("%H:%M"), novo_local, novo_sentido,
                                    novo_sttu, novo_cpre, novos_abordados, novos_removidos
                                )
                                st.session_state.editando_operacao = False
                                st.success("Operação atualizada com sucesso!")
                                st.rerun()

                        if cancelar_edicao:
                            st.session_state.editando_operacao = False
                            st.rerun()

                st.divider()
                st.subheader("⚖️ Tipificações constatadas")

                if detalhes_tipificacoes:
                    tabela_tipificacoes = [{"Código": item["codigo"], "Descrição": item["descricao"], "Quantidade": item["quantidade"]} for item in detalhes_tipificacoes]
                    st.dataframe(tabela_tipificacoes, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhuma tipificação registrada.")

        else:
            st.info("Selecione uma operação na tela '📋 Operações' para visualizar seus detalhes.")