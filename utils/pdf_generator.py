import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def gerar_pdf_relatorio(metricas, operacoes_df, imagem_grafico_periodo=None, imagem_grafico_veiculos=None, imagem_grafico_local=None):
    buffer = io.BytesIO()
    
    # Configuração da página A4 em Modo Retrato com margens de 1.5 cm
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )
    
    elementos = []
    styles = getSampleStyleSheet()
    
    # Estilos customizados para o padrão institucional
    estilo_titulo = ParagraphStyle(
        'TituloInstitucional',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#003366')
    )
    
    estilo_subtitulo = ParagraphStyle(
        'SubTituloInstitucional',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#111111')
    )
    
    estilo_texto_normal = ParagraphStyle(
        'TextoNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#333333')
    )
    
    estilo_cabecalho_tabela = ParagraphStyle(
        'CabecalhoTabela',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        alignment=1,
        textColor=colors.white
    )

    # 1. Cabeçalho Institucional
    elementos.append(Paragraph("PREFEITURA MUNICIPAL DE NATAL • RIO GRANDE DO NORTE", estilo_titulo))
    elementos.append(Paragraph("SECRETARIA MUNICIPAL DE TRÂNSITO E MOBILIDADE URBANA (STTU)", estilo_titulo))
    elementos.append(Paragraph("Setor de Estatística de Acidentes e Trânsito (SEAT)", estilo_subtitulo))
    elementos.append(Spacer(1, 0.2 * cm))
    elementos.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#003366'), spaceAfter=10))
    
    elementos.append(Paragraph("<b>Relatório Gerencial Consolidado de Operações de Blitz</b>", estilo_subtitulo))
    elementos.append(Spacer(1, 0.4 * cm))

    # 2. Seção de Indicadores Gerais
    dados_metricas = [
        [Paragraph("<b>Total de Operações</b>", estilo_texto_normal), Paragraph(f"<b>{metricas.get('total_op', 0)}</b>", estilo_texto_normal),
         Paragraph("<b>Veículos Abordados</b>", estilo_texto_normal), Paragraph(f"<b>{metricas.get('abordados', 0)}</b>", estilo_texto_normal)],
        [Paragraph("<b>Efetivo STTU</b>", estilo_texto_normal), Paragraph(f"{metricas.get('sttu', 0)}", estilo_texto_normal),
         Paragraph("<b>Veículos Removidos</b>", estilo_texto_normal), Paragraph(f"{metricas.get('removidos', 0)}", estilo_texto_normal)],
        [Paragraph("<b>Efetivo CPRE</b>", estilo_texto_normal), Paragraph(f"{metricas.get('cpre', 0)}", estilo_texto_normal),
         Paragraph("<b>Taxa de Remoção</b>", estilo_texto_normal), Paragraph(f"{metricas.get('taxa_remocao', '0%')}", estilo_texto_normal)]
    ]
    
    tabela_metricas = Table(dados_metricas, colWidths=[4.5 * cm, 4 * cm, 4.5 * cm, 4 * cm])
    tabela_metricas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F4F6F9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(tabela_metricas)
    elementos.append(Spacer(1, 0.5 * cm))

    # 3. Adicionando Gráficos (se fornecidos)
    if imagem_grafico_periodo:
        elementos.append(Paragraph("<b>Operações por Período</b>", estilo_texto_normal))
        elementos.append(Spacer(1, 0.1 * cm))
        elementos.append(Image(io.BytesIO(imagem_grafico_periodo), width=15 * cm, height=6 * cm))
        elementos.append(Spacer(1, 0.4 * cm))

    if imagem_grafico_veiculos:
        elementos.append(Paragraph("<b>Veículos Abordados x Removidos</b>", estilo_texto_normal))
        elementos.append(Spacer(1, 0.1 * cm))
        elementos.append(Image(io.BytesIO(imagem_grafico_veiculos), width=12 * cm, height=5 * cm))
        elementos.append(Spacer(1, 0.4 * cm))

    # Quebra de página para organizar a visualização dos locais e tabela
    elementos.append(PageBreak())

    if imagem_grafico_local:
        elementos.append(Paragraph("<b>Operações por Local</b>", estilo_texto_normal))
        elementos.append(Spacer(1, 0.1 * cm))
        elementos.append(Image(io.BytesIO(imagem_grafico_local), width=15 * cm, height=7 * cm))
        elementos.append(Spacer(1, 0.4 * cm))

    # 4. Tabela Resumo das Operações
    elementos.append(Paragraph("<b>Detalhamento das Operações Registradas</b>", estilo_texto_normal))
    elementos.append(Spacer(1, 0.2 * cm))
    
    cabecalho_tabela = [
        Paragraph("ID", estilo_cabecalho_tabela),
        Paragraph("Data", estilo_cabecalho_tabela),
        Paragraph("Local", estilo_cabecalho_tabela),
        Paragraph("Abordados", estilo_cabecalho_tabela),
        Paragraph("Removidos", estilo_cabecalho_tabela)
    ]
    
    dados_tabela = [cabecalho_tabela]
    
    for _, row in operacoes_df.iterrows():
        dados_tabela.append([
            Paragraph(str(row.get('ID', '')), estilo_texto_normal),
            Paragraph(str(row.get('Data', '')), estilo_texto_normal),
            Paragraph(str(row.get('Local', '')), estilo_texto_normal),
            Paragraph(str(row.get('Abordados', 0)), estilo_texto_normal),
            Paragraph(str(row.get('Removidos', 0)), estilo_texto_normal)
        ])
        
    tabela_operacoes = Table(dados_tabela, colWidths=[1.5 * cm, 2.5 * cm, 8 * cm, 2.5 * cm, 2.5 * cm])
    tabela_operacoes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#003366')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FBFD')]),
    ]))
    
    elementos.append(tabela_operacoes)
    
    doc.build(elementos)
    buffer.seek(0)
    return buffer.getvalue()