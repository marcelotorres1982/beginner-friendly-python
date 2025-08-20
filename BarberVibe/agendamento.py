from datetime import datetime, date, time, timedelta

barbeiros = ["Carlos", "Rafael", "João"]

# Agenda agora organizada por data
agenda = {b: {} for b in barbeiros}

# Horários disponíveis (pode ser customizado)
HORARIOS_DISPONIVEIS = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "14:00", "14:30", "15:00", "15:30",
    "16:00", "16:30", "17:00", "17:30", "18:00"
]

SERVICOS = [
    "Corte Simples",
    "Corte + Barba",
    "Apenas Barba",
    "Corte + Barba + Bigode",
    "Tratamento Capilar"
]

def listar_barbeiros():
    return barbeiros

def listar_servicos():
    return SERVICOS

def listar_horarios_disponiveis():
    return HORARIOS_DISPONIVEIS

def listar_agenda_data(barbeiro, data_str):
    """Lista agendamentos de um barbeiro em uma data específica"""
    if data_str not in agenda[barbeiro]:
        return []
    return agenda[barbeiro][data_str]

def listar_toda_agenda(barbeiro):
    """Lista todos os agendamentos de um barbeiro"""
    todos_agendamentos = []
    for data, agendamentos in agenda[barbeiro].items():
        for agendamento in agendamentos:
            agendamento['data'] = data
            todos_agendamentos.append(agendamento)
    
    # Ordenar por data e horário
    todos_agendamentos.sort(key=lambda x: (x['data'], x['horario']))
    return todos_agendamentos

def horarios_ocupados(barbeiro, data_str):
    """Retorna lista de horários ocupados em uma data"""
    if data_str not in agenda[barbeiro]:
        return []
    return [a['horario'] for a in agenda[barbeiro][data_str]]

def horarios_livres(barbeiro, data_str):
    """Retorna horários livres em uma data"""
    ocupados = horarios_ocupados(barbeiro, data_str)
    return [h for h in HORARIOS_DISPONIVEIS if h not in ocupados]

def agendar(barbeiro, cliente, data_str, horario, servico):
    """Agenda um serviço"""
    # Verifica se a data já existe na agenda
    if data_str not in agenda[barbeiro]:
        agenda[barbeiro][data_str] = []
    
    # Verifica se o horário está ocupado
    for a in agenda[barbeiro][data_str]:
        if a['horario'] == horario:
            return False  # horário ocupado
    
    # Adiciona o agendamento
    agenda[barbeiro][data_str].append({
        "cliente": cliente,
        "horario": horario,
        "servico": servico,
        "data_agendamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True

def cancelar_agendamento(barbeiro, data_str, horario):
    """Cancela um agendamento"""
    if data_str in agenda[barbeiro]:
        agenda[barbeiro][data_str] = [
            a for a in agenda[barbeiro][data_str] 
            if a['horario'] != horario
        ]
        return True
    return False

def buscar_cliente(nome_cliente):
    """Busca agendamentos por nome do cliente"""
    resultados = []
    for barbeiro in barbeiros:
        for data, agendamentos in agenda[barbeiro].items():
            for agendamento in agendamentos:
                if nome_cliente.lower() in agendamento['cliente'].lower():
                    resultado = agendamento.copy()
                    resultado['barbeiro'] = barbeiro
                    resultado['data'] = data
                    resultados.append(resultado)
    return resultados