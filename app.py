import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de Efetivo", layout="wide")

st.title("🛡️ Sistema de Gestão de Efetivo")
st.markdown("---")

# --- CONEXÃO COM O GOOGLE SHEETS ---
url_planilha = "https://docs.google.com/spreadsheets/d/1YO5e36Ql7n2SerjL1wO7ZQ33zK06Xhmt9fGwrwqjz3U/edit?gid=1377344967#gid=1377344967"

try:
    # 1. Cria a conexão e lê os dados
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url_planilha, ttl=5)
    
    # 2. Definição dos nomes das colunas (Importante: deixe em MAIÚSCULO aqui)
    col_setor = 'SETOR' 
    col_grupo = 'GRUPO' 
    col_matricula = 'MAT.N'
    col_nome = 'NOME'
    col_posto = 'POSTO'

    # --- TRATAMENTO DE DADOS (O Coração da Solução) ---
    # Normaliza os nomes das colunas da planilha original
    df.columns = df.columns.str.strip().str.upper()

    # Verifica se as colunas básicas existem
    colunas_necessarias = [col_setor, col_grupo, col_matricula, col_nome, col_posto]
    for c in colunas_necessarias:
        if c not in df.columns:
            st.error(f"Coluna '{c}' não encontrada. Colunas atuais: {list(df.columns)}")
            st.stop()

    # Limpeza: Converte tudo para texto e remove vazios (resolve o erro dos menus suspensos)
    for col in colunas_necessarias:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # --- FILTRAGEM ---
    setores_alvo = ['ÁREA S4', 'CORPO DA GUARDA']
    # Filtragem robusta ignorando maiúsculas/minúsculas
    df_filtrado = df[df[col_setor].str.upper().isin(setores_alvo)].copy()

    if df_filtrado.empty:
        st.warning("Nenhum servidor encontrado nos setores ÁREA S4 ou CORPO DA GUARDA.")
    else:
        # --- FUNCIONALIDADE 1: BUSCA POR MATRÍCULA (Sidebar) ---
        st.sidebar.header("🔍 Buscar Servidor")
        matricula_busca = st.sidebar.text_input("Digite a Matrícula Nova:")

        if matricula_busca:
            servidor = df_filtrado[df_filtrado[col_matricula] == matricula_busca.strip()]
            
            if not servidor.empty:
                st.sidebar.success("Servidor Localizado!")
                st.sidebar.markdown(f"**Nome:** {servidor.iloc[0][col_nome]}")
                st.sidebar.markdown(f"**Posto:** {servidor.iloc[0][col_posto]}")
                st.sidebar.markdown(f"**Setor:** {servidor.iloc[0][col_setor]}")
                
                st.info(f"Exibindo resultado para matrícula: {matricula_busca}")
                st.dataframe(servidor)
            else:
                st.sidebar.error("Matrícula não encontrada nos setores selecionados.")

        # --- FUNCIONALIDADE 2: GUIAS POR GRUPO DE SERVIÇO ---
        st.subheader("Visão Geral por Grupo de Serviço")

        # Pegamos grupos que não sejam vazios e ordenamos
        grupos_validos = sorted([g for g in df_filtrado[col_grupo].unique() if g != ""])
        
        if grupos_validos:
            abas = st.tabs(grupos_validos)

            for i, grupo in enumerate(grupos_validos):
                with abas[i]:
                    st.write(f"Servidores do grupo: **{grupo}**")
                    df_grupo = df_filtrado[df_filtrado[col_grupo] == grupo]
                    
                    colunas_exibir = [col_matricula, col_nome, col_posto, col_setor]
                    st.dataframe(df_grupo[colunas_exibir], hide_index=True, use_container_width=True)
                    st.caption(f"Total: {len(df_grupo)} servidores")
        else:
            st.info("Não há grupos de serviço preenchidos para estes setores.")

except Exception as e:
    st.error(f"Erro crítico: {e}")
