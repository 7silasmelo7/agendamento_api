from pydantic import BaseModel
from typing import List
from model.profissional import Agendamento
from datetime import time, date




class AgendamentoSchema(BaseModel):
    """ Define o dia e horário da agenda do profissional com o paciente 
    """
    profissional: str
    paciente: str 
    servico: str 
    valor: float 
    horario: time
    data: date


    


class AgendamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do profissional e do paciente.
    """
    profissional: str
    paciente: str
    


class ListaAgendamentoSchema(BaseModel):
    """ Define uma listagem de profissionais e pacientes será retornada.
    """
    agenda: List[AgendamentoSchema]
    


def apresenta_agenda(agendamentos: List[Agendamento]):
    """ Retorna uma representação da agenda seguindo o schema definido em
        AgendamentoViewSchema.
    """
    result = []
    for agendamento in agendamentos:
        result.append({
            "profissional": agendamento.profissional,
            "paciente": agendamento.paciente,
            "servico": agendamento.servico,
            "valor": agendamento.valor,
            "horario": agendamento.horario.strftime("%H:%M"),
            "data": agendamento.data.strftime("%d-%m-%Y")
        })

    return {"agenda": result}


class AgendamentoViewSchema(BaseModel):
    """ Define como a agenda será retornado: paciente e profissional.
    """
    id: int 
    profissional: str 
    paciente: str 
    servico: str 
    valor: float 
    horario: str 
    data: str
    


class AgendamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    nome: str

def mostra_agenda(agenda: Agendamento):
    """ Retorna uma representação do profissional ou paciente seguindo o schema definido em
        AgendamentoViewSchema.
    """
    return {
        "id": agenda.id,
        "profissional": agenda.profissional,
        "paciente": agenda.paciente,
        "servico": agenda.servico,
        "valor": agenda.valor,
        "horario": agenda.horario.strftime("%H:%M"),
        "data": agenda.data.strftime("%d-%m-%Y"),
        
    }