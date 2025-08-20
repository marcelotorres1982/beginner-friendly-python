import streamlit as st
from datetime import datetime, date, timedelta
from agendamento import (
    listar_barbeiros, listar_servicos, listar_horarios_disponiveis,
    listar_agenda_data, listar_toda_agenda, horarios_livres,
    agendar, cancelar_agendamento, buscar_cliente
)

# Configuração da página
st.set_page_config(
    page_title="BarberVibe",
    page_icon="💈",
    layout="wide"
)

st.title("💈 BarberVibe - Sistema de Agendamentos")

# Sidebar para navegação
st.sidebar.title("Menu")
opcao = st.sidebar.radio(
    "Escolha uma opção:",
    ["📅 Novo Agendamento", "👀 Ver Agendamentos", "🔍 Buscar Cliente", "❌ Cancelar Agendamento"]
)

# ===== NOVO AGENDAMENTO =====
if opcao == "📅 Novo Agendamento":
    st.header("📅 Novo Agendamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        barbeiro = st.selectbox("👨‍💼 Escolha o barbeiro", listar_barbeiros())
        
        # Seletor de data (estilo calendário)
        data_selecionada = st.date_input(
            "📅 Escolha a data",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=30)
        )
        
        data_str = data_selecionada.strftime("%Y-%m-%d")
        
    with col2:
        cliente = st.text_input("👤 Nome do cliente")
        servico = st.selectbox("✂️ Serviço", listar_servicos())
    
    # Mostrar horários disponíveis
    st.subheader(f"⏰ Horários disponíveis para {data_selecionada.strftime('%d/%m/%Y')}")
    
    horarios_livres_dia = horarios_livres(barbeiro, data_str)
    
    if horarios_livres_dia:
        # Organizar horários em colunas
        cols = st.columns(4)
        horario_selecionado = None
        
        for i, horario in enumerate(horarios_livres_dia):
            with cols[i % 4]:
                if st.button(f"🕐 {horario}", key=f"horario_{horario}"):
                    horario_selecionado = horario
        
        # Usar session state para manter a seleção
        if 'horario_escolhido' not in st.session_state:
            st.session_state.horario_escolhido = None
            
        if horario_selecionado:
            st.session_state.horario_escolhido = horario_selecionado
        
        if st.session_state.horario_escolhido:
            st.success(f"✅ Horário selecionado: {st.session_state.horario_escolhido}")
            
            if st.button("📋 Confirmar Agendamento", type="primary"):
                if cliente:
                    if agendar(barbeiro, cliente, data_str, st.session_state.horario_escolhido, servico):
                        st.success("🎉 Agendamento confirmado com sucesso!")
                        st.balloons()
                        st.session_state.horario_escolhido = None
                        st.rerun()
                    else:
                        st.error("⚠️ Erro ao agendar. Horário pode estar ocupado.")
                else:
                    st.warning("⚠️ Por favor, informe o nome do cliente.")
    else:
        st.warning("⚠️ Não há horários disponíveis para esta data.")

# ===== VER AGENDAMENTOS =====
elif opcao == "👀 Ver Agendamentos":
    st.header("👀 Ver Agendamentos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        barbeiro = st.selectbox("👨‍💼 Barbeiro", listar_barbeiros())
    
    with col2:
        tipo_visualizacao = st.radio(
            "Tipo de visualização:",
            ["📅 Por data específica", "📋 Todos os agendamentos"]
        )
    
    if tipo_visualizacao == "📅 Por data específica":
        data_consulta = st.date_input(
            "📅 Data para consulta",
            min_value=date.today() - timedelta(days=30),
            max_value=date.today() + timedelta(days=30)
        )
        
        data_str = data_consulta.strftime("%Y-%m-%d")
        agendamentos = listar_agenda_data(barbeiro, data_str)
        
        st.subheader(f"📅 Agendamentos de {barbeiro} - {data_consulta.strftime('%d/%m/%Y')}")
        
    else:
        agendamentos = listar_toda_agenda(barbeiro)
        st.subheader(f"📋 Todos os agendamentos de {barbeiro}")
    
    if agendamentos:
        for i, agendamento in enumerate(agendamentos):
            with st.expander(f"🕐 {agendamento['horario']} - {agendamento['cliente']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"👤 **Cliente:** {agendamento['cliente']}")
                    st.write(f"⏰ **Horário:** {agendamento['horario']}")
                with col2:
                    st.write(f"✂️ **Serviço:** {agendamento['servico']}")
                    if 'data' in agendamento:
                        data_formatada = datetime.strptime(agendamento['data'], "%Y-%m-%d").strftime("%d/%m/%Y")
                        st.write(f"📅 **Data:** {data_formatada}")
    else:
        st.info("📝 Nenhum agendamento encontrado.")

# ===== BUSCAR CLIENTE =====
elif opcao == "🔍 Buscar Cliente":
    st.header("🔍 Buscar Cliente")
    
    nome_busca = st.text_input("👤 Digite o nome do cliente para buscar:")
    
    if nome_busca:
        resultados = buscar_cliente(nome_busca)
        
        if resultados:
            st.subheader(f"📋 Agendamentos encontrados para '{nome_busca}':")
            
            for resultado in resultados:
                with st.expander(f"📅 {resultado['data']} - {resultado['horario']} ({resultado['barbeiro']})", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"👤 **Cliente:** {resultado['cliente']}")
                        st.write(f"👨‍💼 **Barbeiro:** {resultado['barbeiro']}")
                    with col2:
                        data_formatada = datetime.strptime(resultado['data'], "%Y-%m-%d").strftime("%d/%m/%Y")
                        st.write(f"📅 **Data:** {data_formatada}")
                        st.write(f"⏰ **Horário:** {resultado['horario']}")
                        st.write(f"✂️ **Serviço:** {resultado['servico']}")
        else:
            st.info("📝 Nenhum agendamento encontrado para este cliente.")

# ===== CANCELAR AGENDAMENTO =====
elif opcao == "❌ Cancelar Agendamento":
    st.header("❌ Cancelar Agendamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        barbeiro = st.selectbox("👨‍💼 Barbeiro", listar_barbeiros())
    
    with col2:
        data_cancelamento = st.date_input(
            "📅 Data do agendamento",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=30)
        )
    
    data_str = data_cancelamento.strftime("%Y-%m-%d")
    agendamentos_dia = listar_agenda_data(barbeiro, data_str)
    
    if agendamentos_dia:
        st.subheader("📋 Agendamentos do dia:")
        
        for agendamento in agendamentos_dia:
            col1, col2, col3 = st.columns([3, 3, 1])
            
            with col1:
                st.write(f"🕐 **{agendamento['horario']}**")
            with col2:
                st.write(f"👤 {agendamento['cliente']} - ✂️ {agendamento['servico']}")
            with col3:
                if st.button("❌", key=f"cancel_{agendamento['horario']}", help="Cancelar agendamento"):
                    if cancelar_agendamento(barbeiro, data_str, agendamento['horario']):
                        st.success("✅ Agendamento cancelado!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao cancelar agendamento.")
    else:
        st.info("📝 Nenhum agendamento encontrado para esta data.")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("💈 **BarberVibe** - Sistema de Agendamentos")
st.sidebar.markdown("Desenvolvido para facilitar a gestão da sua barbearia!")