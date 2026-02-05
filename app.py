import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de Efetivo", layout="wide")

st.title("🛡️ Sistema de Gestão de Efetivo")
st.markdown("---")

# --- CONEXÃO COM O GOOGLE SHEETS ---
# Substitua o link abaixo pelo link da sua planilha
url_planilha = "https://docs.google.com/spreadsheets/d/1YO5e36Ql7n2SerjL1wO7ZQ33zK06Xhmt9fGwrwqjz3U/edit?gid=1377344967#gid=1377344967"

try:
    # Cria a conexão
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lê os dados (ttl=5 recarrega a cada 5 segundos se houver mudança, ideal para testes)
    # Se a planilha for privada, precisará configurar o .streamlit/secrets.toml
    df = conn.read(spreadsheet=url_planilha, ttl=5)
    
    # --- TRATAMENTO DE DADOS ---
    # Normalizando nomes das colunas (remove espaços extras e deixa maiúsculo para evitar erros)
    df.columns = df.columns.str.strip().str.upper()
    
    # AJUSTE AQUI: Verifique se os nomes das colunas batem com sua planilha
    # Estou assumindo nomes genéricos, altere conforme sua planilha real
    col_setor = 'SETOR' 
    col_grupo = 'GRUPO' # Ou o nome que estiver na sua planilha
    col_matricula = 'MAT.N'
    col_nome = 'NOME'
    col_posto = 'POSTO'

    # Verifica se as colunas existem para não dar erro
    if col_setor not in df.columns:
        st.error(f"Erro: Não encontrei a coluna '{col_setor}'. As colunas encontradas foram: {list(df.columns)}")
        st.stop()

    # --- FILTRAGEM DOS SETORES ---
    # Filtra apenas ÁREA S4 e CORPO DA GUARDA
    setores_alvo = ['ÁREA S4', 'CORPO DA GUARDA']
    # O comando abaixo filtra onde a coluna SETOR é igual a um dos alvos
    df_filtrado = df[df[col_setor].isin(setores_alvo)]

    if df_filtrado.empty:
        st.warning("Nenhum servidor encontrado nesses setores.")
    else:
        # --- FUNCIONALIDADE 1: BUSCA POR MATRÍCULA ---
        st.sidebar.header("🔍 Buscar Servidor")
        matricula_busca = st.sidebar.text_input("Digite a Matrícula Nova:")

        if matricula_busca:
            # Busca exata (transforma em string para garantir)
            servidor = df_filtrado[df_filtrado[col_matricula].astype(str) == matricula_busca]
            
            if not servidor.empty:
                st.sidebar.success("Servidor Localizado!")
                st.sidebar.markdown(f"**Nome:** {servidor.iloc[0][col_nome]}")
                st.sidebar.markdown(f"**Posto:** {servidor.iloc[0][col_posto]}")
                st.sidebar.markdown(f"**Setor:** {servidor.iloc[0][col_setor]}")
                
                # Destaca na tela principal também
                st.info(f"Exibindo resultado para matrícula: {matricula_busca}")
                st.dataframe(servidor)
            else:
                st.sidebar.error("Matrícula não encontrada nos setores selecionados.")

        # --- FUNCIONALIDADE 2: GUIAS POR GRUPO DE SERVIÇO ---
        st.subheader("Visão Geral por Grupo de Serviço")

        # Pega todos os grupos únicos encontrados no filtro
        grupos_unicos = df_filtrado[col_grupo].unique()
        
        if len(grupos_unicos) > 0:
            # Cria as abas automaticamente baseado nos grupos que existem
            abas = st.tabs(list(grupos_unicos))

            for i, grupo in enumerate(grupos_unicos):
                with abas[i]:
                    st.write(f"Servidores do grupo: **{grupo}**")
                    
                    # Filtra apenas os dados desse grupo
                    df_grupo = df_filtrado[df_filtrado[col_grupo] == grupo]
                    
                    # Seleciona apenas as colunas que você quer mostrar
                    colunas_exibir = [col_matricula, col_nome, col_posto, col_setor]
                    
                    # Mostra a tabela limpa (hide_index esconde a numeração lateral padrão do pandas)
                    st.dataframe(df_grupo[colunas_exibir], hide_index=True, use_container_width=True)
                    
                    st.caption(f"Total: {len(df_grupo)} servidores")
        else:
            st.info("Não há grupos de serviço definidos para estes setores.")

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar a planilha: {e}")
    st.markdown("Dica: Verifique se a planilha está compartilhada corretamente ou se os nomes das colunas estão certos.")
