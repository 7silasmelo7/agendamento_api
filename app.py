from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from schemas import ErrorSchema

from model import Session, Agendamento
from logger import logger
from schemas import AgendamentoSchema, AgendamentoBuscaSchema, ListaAgendamentoSchema, AgendamentoViewSchema, AgendamentoDelSchema, mostra_agenda, apresenta_agenda
from flask_cors import CORS
from sqlalchemy import func
from datetime import date
from sqlalchemy import or_
from flask import request



info = Info(title="Agenda API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
agenda_tag = Tag(name="Agendamento", description="Adição, visualização e remoção de clientes à base")





@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/agendamento', tags=[agenda_tag],
          responses={"200": AgendamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_agenda(form: AgendamentoSchema):
    """Adiciona um novo cliente e respectivo profissional que irá atendê-lo"""

    # valida data e horário
    try:
        data_obj = form.data
        horario_obj = form.horario
    except ValueError:
        return {"mensagem": "Formato de data ou horário inválido. Use 'YYYY-MM-DD' e 'HH:MM'."}, 400
    
    # impede a inserção de datas passadas
    hoje = date.today()
    if data_obj < hoje:
        return {"mensagem": "Não é permitido fazer agendamento "
        "com data retroativa."}, 400
    
    # impede a inserção de horários retroativos para o mesmo dia
    agora = datetime.now().time()
    if data_obj == hoje and horario_obj < agora:
        return {"mensagem": "Não é permitido fazer agendamento "
        "com horário retroativo."}, 400

    # cria sessão ANTES de qualquer uso
    session = Session()

    try:
        # Verifica se há conflito de data e horário na agenda
        conflito = session.query(Agendamento).filter(
            func.lower(Agendamento.profissional) == form.profissional.lower(),
            Agendamento.data == data_obj,
            Agendamento.horario == horario_obj
        ).first()

        if conflito:
            return {
                "mensagem": "Este profissional já possui um agendamento neste dia e horário."
            }, 409

        # cria o objeto Agendamento
        agenda = Agendamento(
            profissional=form.profissional,
            paciente=form.paciente,
            servico=form.servico,
            valor=form.valor,
            horario=horario_obj,
            data=data_obj
        )

        logger.debug(
            f"Novo agendamento recebido profissional = {agenda.profissional} "
            f"paciente = {agenda.paciente} servico = {agenda.servico} "
            f"valor = {agenda.valor} horario = {agenda.horario}"
        )

        # adiciona e salva no banco
        session.add(agenda)
        session.commit()

        logger.debug(
            f"Agendamento confirmado : profissional = {agenda.profissional} "
            f"paciente = {agenda.paciente} horario = {agenda.horario}"
        )

        return mostra_agenda(agenda), 200

    except IntegrityError:
        session.rollback()
        error_msg = "Já existe agendamento salvo para este dia e horário."
        logger.warning(error_msg)
        return {"mensagem": error_msg}, 409

    except Exception as e:
        session.rollback()
        logger.exception(f"Erro ao salvar agendamento: {e}")
        return {"mensagem": "Não foi possível salvar o agendamento."}, 400

    finally:
        session.close()



@app.get('/agendamentos', tags=[agenda_tag],
         responses={"200": ListaAgendamentoSchema, "404": ErrorSchema})
def get_agenda_lista():
    """Faz a busca na agenda de pacientes e profissionais agendados

    Retorna uma representação da agenda
    """
    logger.debug(f"Coletando_dados ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    agendamentos = session.query(Agendamento).all()
    session.close()

    if not agendamentos:
        # se não há agendamentos cadastrados
        return {"agenda": []}, 200
    else:
        logger.debug(f"%d agendamentos encontrados" % len(agendamentos))
        # retorna a representação de agenda
        
        return apresenta_agenda(agendamentos), 200
    



@app.get('/agendamento', tags=[agenda_tag],
         responses={"200": ListaAgendamentoSchema, "404": ErrorSchema})
def get_agenda_busca(profissional: str = None, paciente: str = None):
    """
    Busca agendamentos por profissional OU paciente.
    Lê parâmetros diretamente de request.args para evitar problemas de binding.
    """
    session = Session()
    query = session.query(Agendamento)
    filtros = []

    # pega os parâmetros diretamente do request (fallback seguro)
    q_prof = request.args.get('profissional') or profissional
    q_pac = request.args.get('paciente') or paciente

    # normaliza e ignora termos vazios
    if q_prof:
        termo_prof = unquote(unquote(q_prof)).strip()
        if termo_prof:
            filtros.append(func.lower(func.trim(Agendamento.profissional)).like(f"%{termo_prof.lower()}%"))
            logger.debug(f"Filtro profissional: '{termo_prof}'")

    if q_pac:
        termo_pac = unquote(unquote(q_pac)).strip()
        if termo_pac:
            filtros.append(func.lower(func.trim(Agendamento.paciente)).like(f"%{termo_pac.lower()}%"))
            logger.debug(f"Filtro paciente: '{termo_pac}'")

    if filtros:
        query = query.filter(or_(*filtros))
        logger.debug("Aplicado OR nos filtros.")
    else:
        logger.debug("Nenhum filtro válido; query sem WHERE.")

    # log do SQL final (útil para debug)
    try:
        logger.debug("SQL final: %s", str(query.statement.compile(compile_kwargs={"literal_binds": True})))
    except Exception as e:
        logger.debug("Não foi possível compilar SQL para debug: %s", e)

    resultados = query.all()
    session.close()

    if not resultados:
        return {"mensagem": "Nenhum agendamento foi encontrado."}, 404

    return apresenta_agenda(resultados), 200



@app.delete('/agendamento', tags=[agenda_tag],
            responses={"200": AgendamentoDelSchema, "404": ErrorSchema})
def del_agendamento(query: AgendamentoBuscaSchema):
    """Deleta um agendamento a partir do nome do profissional + paciente informado

    Retorna uma mensagem de confirmação da remoção.
    """

    profissional = query.profissional
    paciente = query.paciente


    print(">>> PROF:", repr(profissional))
    print(">>> PAC:", repr(paciente))

    profissional_nome = (profissional or "").strip().lower()
    paciente_nome = (paciente or "").strip().lower()
    
    logger.debug(f"Deletando dados sobre profissional #{profissional_nome}")
    logger.debug(f"Deletando dados sobre paciente #{paciente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção

    registros = session.query(Agendamento).filter(
        func.lower(func.trim(Agendamento.profissional)) == profissional_nome,
        func.lower(func.trim(Agendamento.paciente)) == paciente_nome
    ).all()

    if not registros:
        session.close()
        return {"mensagem": "Agendamento não encontrado"}, 404
    
    for r in registros:
        session.delete(r)
    
    session.commit()
    session.close()

    return {
        "mensagem": "Agendamento removido", "nome": f"{profissional} - {paciente}"
    }, 200

    


