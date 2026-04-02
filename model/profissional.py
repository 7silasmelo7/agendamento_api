from sqlalchemy import Column, String, Integer, DateTime, Float, Time, Date, UniqueConstraint
from datetime import datetime
from typing import Union

from  model import Base


class Agendamento(Base):
    __tablename__ = 'agenda'

    id = Column("pk_agenda", Integer, primary_key=True)
    data_insercao = Column(DateTime, default=datetime.now)
    profissional = Column(String(140), nullable = False)
    paciente = Column(String(140), nullable = False)
    servico = Column(String(140), nullable = False)
    valor = Column(Float, nullable = False)
    horario = Column(Time, nullable = False)
    data = Column(Date, nullable = False)

    __table_args__ = (UniqueConstraint('profissional', 'data', 'horario', name = 'uix_prof_data_horario'),)
    

   

    def __init__(self, profissional: str, paciente: str, servico: str, 
                 valor: float, horario, data, data_insercao: Union[datetime, None] = None
                 ):
        """
        Cria uma agenda de um serviço prestado por um profissional a um paciente, 
        com o valor do serviço e a data de inserção da agenda.

        Arguments:
            profissional: nome do profissional.
            paciente: nome do paciente.
            servico: descrição do serviço prestado.
            valor: valor do serviço.
            data_insercao: data no momento em que a informação é inserida no banco de dados
            data: em que o serviço foi agendado
        """
        self.profissional = profissional
        self.paciente = paciente
        self.servico = servico
        self.valor = valor
        self.horario = horario
        self.data = data

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

 