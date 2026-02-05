# import streamlit as st
# import pandas as pd
# from streamlit_gsheets import GSheetsConnection

# # --- CONFIGURAÇÃO DA PÁGINA ---
# st.set_page_config(page_title="Sistema de Efetivo", layout="wide")

# st.title("🛡️ Sistema de Gestão de Efetivo")
# st.markdown("---")

# # --- CONEXÃO COM O GOOGLE SHEETS ---
# url_planilha = "https://docs.google.com/spreadsheets/d/1YO5e36Ql7n2SerjL1wO7ZQ33zK06Xhmt9fGwrwqjz3U/edit?gid=1377344967#gid=1377344967"

# try:
#     # 1. Cria a conexão e lê os dados
#     conn = st.connection("gsheets", type=GSheetsConnection)
#     df = conn.read(spreadsheet=url_planilha, ttl=5)
    
#     # 2. Definição dos nomes das colunas (Importante: deixe em MAIÚSCULO aqui)
#     col_setor = 'SETOR' 
#     col_grupo = 'GRUPO' 
#     col_matricula = 'MAT.N'
#     col_nome = 'NOME'
#     col_posto = 'POSTO'

#     # --- TRATAMENTO DE DADOS (O Coração da Solução) ---
#     # Normaliza os nomes das colunas da planilha original
#     df.columns = df.columns.str.strip().str.upper()

#     # Verifica se as colunas básicas existem
#     colunas_necessarias = [col_setor, col_grupo, col_matricula, col_nome, col_posto]
#     for c in colunas_necessarias:
#         if c not in df.columns:
#             st.error(f"Coluna '{c}' não encontrada. Colunas atuais: {list(df.columns)}")
#             st.stop()

#     # Limpeza: Converte tudo para texto e remove vazios (resolve o erro dos menus suspensos)
#     for col in colunas_necessarias:
#         df[col] = df[col].fillna("").astype(str).str.strip()

#     # --- FILTRAGEM ---
#     setores_alvo = ['ÁREA S4', 'CORPO DA GUARDA']
#     # Filtragem robusta ignorando maiúsculas/minúsculas
#     df_filtrado = df[df[col_setor].str.upper().isin(setores_alvo)].copy()

#     if df_filtrado.empty:
#         st.warning("Nenhum servidor encontrado nos setores ÁREA S4 ou CORPO DA GUARDA.")
#     else:
#         # --- FUNCIONALIDADE 1: BUSCA POR MATRÍCULA (Sidebar) ---
#         st.sidebar.header("🔍 Buscar Servidor")
#         matricula_busca = st.sidebar.text_input("Digite a Matrícula Nova:")

#         if matricula_busca:
#             servidor = df_filtrado[df_filtrado[col_matricula] == matricula_busca.strip()]
            
#             if not servidor.empty:
#                 st.sidebar.success("Servidor Localizado!")
#                 st.sidebar.markdown(f"**Nome:** {servidor.iloc[0][col_nome]}")
#                 st.sidebar.markdown(f"**Posto:** {servidor.iloc[0][col_posto]}")
#                 st.sidebar.markdown(f"**Setor:** {servidor.iloc[0][col_setor]}")
                
#                 st.info(f"Exibindo resultado para matrícula: {matricula_busca}")
#                 st.dataframe(servidor)
#             else:
#                 st.sidebar.error("Matrícula não encontrada nos setores selecionados.")

#         # --- FUNCIONALIDADE 2: GUIAS POR GRUPO DE SERVIÇO ---
#         st.subheader("Visão Geral por Grupo de Serviço")

#         # Pegamos grupos que não sejam vazios e ordenamos
#         grupos_validos = sorted([g for g in df_filtrado[col_grupo].unique() if g != ""])
        
#         if grupos_validos:
#             abas = st.tabs(grupos_validos)

#             for i, grupo in enumerate(grupos_validos):
#                 with abas[i]:
#                     st.write(f"Servidores do grupo: **{grupo}**")
#                     df_grupo = df_filtrado[df_filtrado[col_grupo] == grupo]
                    
#                     colunas_exibir = [col_matricula, col_nome, col_posto, col_setor]
#                     st.dataframe(df_grupo[colunas_exibir], hide_index=True, use_container_width=True)
#                     st.caption(f"Total: {len(df_grupo)} servidores")
#         else:
#             st.info("Não há grupos de serviço preenchidos para estes setores.")

# ---------------------Versão 2 -----------------------------------
# import streamlit as st
# import pandas as pd
# from streamlit_gsheets import GSheetsConnection

# # --- CONFIGURAÇÃO E CONEXÃO (Mantida) ---
# st.set_page_config(page_title="Sistema de Efetivo", layout="wide")
# url_planilha = "https://docs.google.com/spreadsheets/d/1YO5e36Ql7n2SerjL1wO7ZQ33zK06Xhmt9fGwrwqjz3U/edit?gid=1377344967#gid=1377344967"

# try:
#     conn = st.connection("gsheets", type=GSheetsConnection)
#     df = conn.read(spreadsheet=url_planilha, ttl=5)
    
#     # Padronização de Colunas
#     df.columns = df.columns.str.strip().str.upper()
    
#     # Definição das variáveis de coluna (incluindo ESCALA)
#     col_setor = 'SETOR' 
#     col_grupo = 'GRUPO' 
#     col_matricula = 'MAT.N'
#     col_nome = 'NOME'
#     col_posto = 'POSTO'
#     col_escala = 'ESCALA' # Nova variável solicitada

#     # Limpeza de dados (converte para string e remove espaços)
#     for col in [col_setor, col_grupo, col_matricula, col_nome, col_posto, col_escala]:
#         df[col] = df[col].fillna("").astype(str).str.strip()
#     # ... (conexão e padronização das colunas mantidas)
    
#     # --- FILTRAGEM DINÂMICA NA BARRA LATERAL ---
#     st.sidebar.header("⚙️ Filtros de Acesso")
    
#     # Busca todos os setores únicos da planilha para criar o menu
#     lista_setores = sorted(df[col_setor].unique())
    
#     # Caixa de seleção múltipla (Multiselect)
#     setores_escolhidos = st.sidebar.multiselect(
#         "Selecione o(s) Setor(es):",
#         options=lista_setores,
#         default=[s for s in ['ÁREA S4', 'CORPO DA GUARDA'] if s in lista_setores]
#     )

#     # Filtragem Base: Tudo o que fizermos abaixo será baseado APENAS nos setores escolhidos
#     df_base = df[df[col_setor].isin(setores_escolhidos)].copy()

#     # --- LÓGICA DE FILTRAGEM PERSONALIZADA (Baseada no df_base) ---
#     # 1. Guia SUPERVISÃO
#     df_supervisao = df_base[df_base[col_posto].isin(postos_supervisao)]

#     # 2. Guia CORPO DA GUARDA
#     df_cg = df_base[df_base[col_setor] == "CORPO DA GUARDA"]

#     # ... (continue com os filtros df_alpha, df_bravo, etc., usando df_base)

#     # --- LÓGICA DE FILTRAGEM PERSONALIZADA ---
    
#     # 1. Guia SUPERVISÃO (Filtro por Postos Específicos)
#     postos_supervisao = [
#         "VTR DE APOIO - AS4", 
#         "VTR DO ENCARREGADO - AS4", 
#         "ENCARREGADO(A) - AS4", 
#         "SUPERVISOR(A) CHS"
#     ]
#     df_supervisao = df[df[col_posto].isin(postos_supervisao)]

#     # 2. Guia CORPO DA GUARDA (Filtro por Setor)
#     df_cg = df[df[col_setor] == "CORPO DA GUARDA"]

#     # 3. Guia ESCALA 12X60 (Filtro pela nova coluna)
#     df_12x60 = df[df[col_escala] == "12X60"]

#     # 4. Guias ALPHA, BRAVO, CHARLIE, DELTA (Filtro por Grupo)
#     # Aqui filtramos quem NÃO está nos grupos acima para não duplicar, se desejar
#     df_alpha = df[df[col_grupo] == "A"]
#     df_bravo = df[df[col_grupo] == "B"]
#     df_charlie = df[df[col_grupo] == "C"]
#     df_delta = df[df[col_grupo] == "D"]

#     # --- CRIAÇÃO DA INTERFACE EM ABAS ---
#     st.title("🛡️ Gestão de Efetivo - Visualização Operacional")
    
#     # Criamos a lista de nomes das abas conforme sua necessidade
#     nomes_abas = ["SUPERVISÃO", "CORPO DA GUARDA", "ESCALA 12X60", "ALPHA", "BRAVO", "CHARLIE", "DELTA"]
#     abas = st.tabs(nomes_abas)

#     # Dicionário para facilitar a iteração: Nome da Aba -> DataFrame correspondente
#     mapa_dados = {
#         "SUPERVISÃO": df_supervisao,
#         "CORPO DA GUARDA": df_cg,
#         "ESCALA 12X60": df_12x60,
#         "ALPHA": df_alpha,
#         "BRAVO": df_bravo,
#         "CHARLIE": df_charlie,
#         "DELTA": df_delta
#     }

#     for i, nome_aba in enumerate(nomes_abas):
#         with abas[i]:
#             dados_aba = mapa_dados[nome_aba]
#             st.subheader(f"Efetivo: {nome_aba}")
            
#             if not dados_aba.empty:
#                 # Exibição da tabela
#                 st.dataframe(
#                     dados_aba[[col_matricula, col_nome, col_posto, col_grupo, col_escala]], 
#                     hide_index=True, 
#                     use_container_width=True
#                 )
#                 st.caption(f"Total nesta guia: {len(dados_aba)} servidores")
#             else:
#                 st.info(f"Nenhum registro encontrado para {nome_aba}.")

# except Exception as e:
#     st.error(f"Erro ao processar filtros: {e}")
# # except Exception as e:
# #     st.error(f"Erro crítico: {e}")

# ---------------------Versão 3 -----------------------------------
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO E CONEXÃO ---
st.set_page_config(page_title="Sistema de Efetivo", layout="wide")
url_planilha = "https://docs.google.com/spreadsheets/d/1YO5e36Ql7n2SerjL1wO7ZQ33zK06Xhmt9fGwrwqjz3U/edit?gid=1377344967#gid=1377344967"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url_planilha, ttl=5)
    
    # 1. Padronização de Colunas
    df.columns = df.columns.str.strip().str.upper()
    
    col_setor = 'SETOR' 
    col_grupo = 'GRUPO' 
    col_matricula = 'MAT.N'
    col_nome = 'NOME'
    col_posto = 'POSTO'
    col_escala = 'ESCALA'

    # 2. Limpeza de dados
    colunas_foco = [col_setor, col_grupo, col_matricula, col_nome, col_posto, col_escala]
    for col in colunas_foco:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # --- FILTRAGEM DINÂMICA NA BARRA LATERAL ---
    st.sidebar.header("⚙️ Filtros de Acesso")
    lista_setores = sorted(df[col_setor].unique())
    
    setores_escolhidos = st.sidebar.multiselect(
        "Selecione o(s) Setor(es):",
        options=lista_setores,
        default=[s for s in ['ÁREA S4', 'CORPO DA GUARDA'] if s in lista_setores]
    )

    # Criamos o df_base que servirá para todos os filtros abaixo
    df_base = df[df[col_setor].isin(setores_escolhidos)].copy()

    # --- LÓGICA DE FILTRAGEM PERSONALIZADA (Ordem corrigida) ---
    
    # Definimos a lista ANTES de usar no filtro (Resolve o erro que você teve)
    postos_supervisao = [
        "VTR DE APOIO - AS4", 
        "VTR DO ENCARREGADO - AS4", 
        "ENCARREGADO(A) - AS4", 
        "SUPERVISOR(A) CHS"
    ]

    # Agora sim aplicamos os filtros usando o df_base
    df_supervisao = df_base[df_base[col_posto].isin(postos_supervisao)]
    df_cg = df_base[df_base[col_setor] == "CORPO DA GUARDA"]
    df_12x60 = df_base[df_base[col_escala] == "12X60"]
    
    # Filtros por Grupo
    df_alpha = df_base[df_base[col_grupo] == "A"]
    df_bravo = df_base[df_base[col_grupo] == "B"]
    df_charlie = df_base[df_base[col_grupo] == "C"]
    df_delta = df_base[df_base[col_grupo] == "D"]

    # --- INTERFACE EM ABAS ---
    st.title("🛡️ Gestão de Efetivo - Visualização Operacional")
    
    nomes_abas = ["SUPERVISÃO", "CORPO DA GUARDA", "ESCALA 12X60", "ALPHA", "BRAVO", "CHARLIE", "DELTA"]
    abas = st.tabs(nomes_abas)

    mapa_dados = {
        "SUPERVISÃO": df_supervisao,
        "CORPO DA GUARDA": df_cg,
        "ESCALA 12X60": df_12x60,
        "ALPHA": df_alpha,
        "BRAVO": df_bravo,
        "CHARLIE": df_charlie,
        "DELTA": df_delta
    }

    for i, nome_aba in enumerate(nomes_abas):
        with abas[i]:
            dados_aba = mapa_dados[nome_aba]
            st.subheader(f"Efetivo: {nome_aba}")
            
            if not dados_aba.empty:
                st.dataframe(
                    dados_aba[[col_matricula, col_nome, col_posto, col_grupo, col_escala]], 
                    hide_index=True, 
                    use_container_width=True
                )
                st.caption(f"Total nesta guia: {len(dados_aba)} servidores")
            else:
                st.info(f"Nenhum registro encontrado para {nome_aba} nos setores selecionados.")

except Exception as e:
    st.error(f"Erro ao processar filtros: {e}")
