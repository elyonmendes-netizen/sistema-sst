import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de SST", page_icon="🛡️", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA (Mantendo o Design Limpo) ---
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; margin-bottom: 1rem; }
    .card { background-color: #F3F4F6; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid #1E3A8A; }
    .card h3 { margin-top: 0; color: #1E3A8A; }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE USUÁRIOS E SENHAS (Simples para validação) ---
USUARIOS_PERMITIDOS = {
    "admin": {"senha": "admin123", "perfil": "Administrador"},
    "tecnico": {"senha": "sst456", "perfil": "Técnico de Segurança"},
    "colaborador": {"senha": "user789", "perfil": "Colaborador"}
}

# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO (Session State) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "perfil" not in st.session_state:
    st.session_state.perfil = None
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = ""

# --- SIDEBAR: LOGIN E LOGOUT ---
with st.sidebar:
    st.title("🔑 Controle de Acesso")
    
    if not st.session_state.autenticado:
        st.subheader("Efetue o Login")
        usuario_input = st.text_input("Usuário").strip().lower()
        senha_input = st.text_input("Senha", type="password")
        
        if st.button("Entrar", use_container_width=True):
            if usuario_input in USUARIOS_PERMITIDOS and USUARIOS_PERMITIDOS[usuario_input]["senha"] == senha_input:
                st.session_state.autenticado = True
                st.session_state.perfil = USUARIOS_PERMITIDOS[usuario_input]["perfil"]
                st.session_state.usuario_logado = usuario_input
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
    else:
        st.success(f"Conectado como:\n**{st.session_state.perfil}**")
        st.caption(f"Usuário ativo: {st.session_state.usuario_logado}")
        
        st.write("---")
        if st.button("Sair / Logout", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.perfil = None
            st.session_state.usuario_logado = ""
            st.rerun()

# --- CONTEÚDO PRINCIPAL (Renderização Condicional) ---

# 1. TELA DE BLOQUEIO (Caso não esteja logado)
if not st.session_state.autenticado:
    st.markdown('<p class="main-title">🛡️ Sistema de Gestão Integrada (SST)</p>', unsafe_allow_html=True)
    st.warning("🔒 Acesso restrito. Por favor, insira suas credenciais na barra lateral para continuar.")
    
    # Painel expansível para ajudar nos seus testes de desenvolvimento
    with st.expander("ℹ️ Credenciais de Teste (Clique para visualizar)"):
        st.markdown("""
        * **Administrador:** Usuário: `admin` | Senha: `admin123`
        * **Técnico de Segurança:** Usuário: `tecnico` | Senha: `sst456`
        * **Colaborador:** Usuário: `colaborador` | Senha: `user789`
        """)

# 2. TELA: ADMINISTRADOR
elif st.session_state.perfil == "Administrador":
    st.markdown('<p class="main-title">📊 Painel do Administrador</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>📈 Métricas Gerais de SST</h3>
            <p>Visão global de conformidade das NRs, treinamentos vencidos e planos de ação em aberto.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>⚙️ Gerenciar Usuários e Permissões</h3>
            <p>Área destinada ao cadastro de novos colaboradores, alteração de senhas e logs de auditoria.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.subheader("📋 Logs de Envio Recentes (Google Sheets)")
    st.info("Aqui você pode renderizar o `st.dataframe()` conectado à sua planilha principal para auditoria completa.")

# 3. TELA: TÉCNICO DE SEGURANÇA
elif st.session_state.perfil == "Técnico de Segurança":
    st.markdown('<p class="main-title">📋 Área do Técnico - Inspeções e NRs</p>', unsafe_allow_html=True)
    st.write("Insira os dados coletados em campo para alimentar automaticamente os relatórios e o Google Sheets.")
    
    # Formulário estruturado de coleta
    with st.form("form_inspecao_sst"):
        st.subheader("Nova Avaliação de Campo (NR 1 / LTCAT)")
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            setor = st.text_input("Setor Avaliado", placeholder="Ex: Produção, Almoxarifado...")
            responsavel = st.text_input("Responsável pelo Setor")
        with col_form2:
            risco = st.selectbox("Risco Preponderante", ["Físico", "Químico", "Biológico", "Ergonômico", "Acidente"])
            status_nr = st.radio("Conformidade com a NR 1", ["Conforme", "Não Conforme", "Requer Plano de Ação"], horizontal=True)
            
        descricao_divergencia = st.text_area("Descrição detalhada / Observações")
        
        enviar = st.form_submit_button("Gravar e Enviar Dados")
        
        if enviar:
            # Aqui entra a sua lógica de integração com o Apps Script do Google Sheets
            st.success("✅ Dados registrados com sucesso e enviados para a planilha central!")

# 4. TELA: COLABORADOR
elif st.session_state.perfil == "Colaborador":
    st.markdown('<p class="main-title">👋 Área do Colaborador</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>📢 Comunicados Importantes de Segurança</h3>
        <p>Atenção à obrigatoriedade do uso de EPIs no setor de expedição durante este turno. Segurança em primeiro lugar!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🛠️ Minhas Opções")
    col_colab1, col_colab2 = st.columns(2)
    with col_colab1:
        if st.button("🚨 Relatar Quase-Acidente / Sugestão", use_container_width=True):
            st.info("Funcionalidade para abrir um formulário simples de desvio de segurança.")
    with col_colab2:
        if st.button("📅 Meus Treinamentos Agendados", use_container_width=True):
            st.info("Visualização das próximas reciclagens obrigatórias de NRs.")
