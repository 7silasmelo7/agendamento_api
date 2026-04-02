📘 Agenda API – Sistema de Agendamentos

API REST desenvolvida em Python + Flask, utilizando SQLite como banco de dados e documentada com Swagger (OpenAPI).
O sistema permite cadastrar, listar, buscar e remover agendamentos de profissionais com seus respectivos pacientes.

## 🚀 Tecnologias Utilizadas

![Python 3.12](https://img.shields.io/badge/Python%203.12-6d28d9
)
![Flask](https://img.shields.io/badge/Flask-6d28d9
)
![Flask-OpenAPI3 (Swagger)](https://img.shields.io/badge/Flask-OpenAPI3%20(Swagger)-6d28d9)

![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-6d28d9
)

![SQLite](https://img.shields.io/badge/SQLite-6d28d9
)

![Pydantic](https://img.shields.io/badge/Pydantic-6d28d9
)

![Flask-CORS](https://img.shields.io/badge/Flask-CORS-6d28d9)

## 📂 Estrutura do Projeto

![App Screenshot](https://i.ibb.co/V0BbMHcM/Captura-de-tela-2026-04-01-101919.png)

## 🗄️ Banco de Dados

A API utiliza SQLite, criado automaticamente na pasta  ao iniciar o servidor.



| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer PK` | Identificador |
| `profissional` | `string` | Nome do profissional |
| `paciente` | `string` | Nome do paciente |
| `servico` | `string` | Serviço prestado |
| `valor` | `float` | Valor cobrado |
| `horario` | `time` | Horário do atendimento |
| `data` | `date` | Data do atendimento |
| `data_insercao` | `datetime` | Registro no banco de dados |


#### OBS: Restrição de unicidade para profissional, data e horário, evitando assim agendamentos duplicados.

## 📌 Rotas da API

🔹 1. Criar agendamento

POST /agendamento

Corpo da requisição:

![App Screenshot](https://i.ibb.co/gMwj4t4Q/Captura-de-tela-2026-04-02-081506.png)

Respostas:

• 	200 – Agendamento criado

• 	400 – Dados inválidos

• 	409 – Conflito de horário

🔹 2. Listar todos os agendamentos

GET /agendamentos

Corpo da requisição:

![App Screenshot](https://i.ibb.co/F4t6kJGv/Captura-de-tela-2026-04-02-080646.png)

Respostas:

• 	200 – Ok

🔹 3. Buscar por profissional ou paciente

GET /agendamento?profissional=lanna&paciente=lanna

![App Screenshot](https://i.ibb.co/Zbh5m3J/Captura-de-tela-2026-04-02-083138.png)


GET /agendamento?profissional=carol&paciente=carol

![App Screenshot](https://i.ibb.co/MkQpZQfk/Captura-de-tela-2026-04-02-083447.png)

Respostas:

• 	200 – OK

• 	404 – Nenhum agendamento encontrado


🔹 4. Remover agendamento
DELETE /agendamento?profissional=Ana&paciente=Carlos

• 	200 – Removido !

## 📄 Documentação Swagger

A documentação completa está disponível automaticamente em:

```bash
  http://localhost:5000/openapi


## 🛠️ Como Executar o Projeto

1. Criar ambiente virtual (recomendado)

```bash
  python -m venv venv
```

2. Ativar o ambiente virtual

```bash
  venv\Scripts\Activate
```

3. Instalar dependências

```bash
  pip install -r requirements.txt
```

4. Executar a API

```bash
  flask run --host 0.0.0.0 --port 5000
```

5. Executar a API em modo desenvolvimento

```bash
  flask run --host 0.0.0.0 --port 5000 --reload
```

## 📝 Logs

Os logs são gerados automaticamente em:

```bash
  C:/temp/agendamento_logs/
```
Arquivos:

• 	error.log 

• 	detailed.log





