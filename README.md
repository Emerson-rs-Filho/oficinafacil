# OficinaFácil

Sistema web de **agendamento e ordens de serviço para pequenas oficinas mecânicas**.
Projeto Integrador Transdisciplinar em Sistemas de Informação II — Situação-Problema 2.

- **Front-end:** HTML5, CSS3 (responsivo) e JavaScript puro
- **Back-end:** Python 3 + Flask, no padrão **MVC**
- **Banco de dados:** SQLite (padrão) ou MySQL (script em `database/schema_mysql.sql`)
- **ORM:** SQLAlchemy · **Autenticação:** Flask-Login (senhas com hash)

## Funcionalidades

- Cadastro e login de usuários
- Painel com indicadores (clientes, veículos, ordens em aberto, faturamento) e agenda do dia
- CRUD de clientes, com busca e máscara de telefone/CPF
- CRUD de veículos, com validação de placa (antiga e Mercosul)
- CRUD de ordens de serviço, com filtro por status e troca rápida de status sem recarregar a página

## Estrutura (MVC)

```
oficinafacil/
├── app/
│   ├── models/          # MODEL: Usuario, Cliente, Veiculo, OrdemServico
│   ├── controllers/     # CONTROLLER: rotas e regras de negócio (Blueprints)
│   └── views/
│       ├── templates/   # VIEW: páginas HTML (Jinja2)
│       └── static/      # VIEW: CSS e JavaScript
├── database/schema_mysql.sql   # projeto físico do banco
├── tests/test_app.py           # testes automatizados
├── config.py  run.py  seed.py  requirements.txt
```

## Como rodar no seu computador

Pré-requisito: Python 3.10 ou superior.

```bash
cd oficinafacil
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python seed.py                 # opcional: cria dados de exemplo
python run.py
```

Acesse http://127.0.0.1:5000 — login de exemplo: **admin@oficina.com / admin123**

Rodar os testes: `python -m pytest`

### Usando MySQL (opcional)

1. Execute `database/schema_mysql.sql` no MySQL Workbench.
2. Antes de rodar, defina: `set DATABASE_URL=mysql+pymysql://usuario:senha@localhost/oficinafacil`

## Hospedagem gratuita (PythonAnywhere)

1. Crie uma conta gratuita em https://www.pythonanywhere.com
2. Em **Files**, envie o projeto (zip) e descompacte pelo console Bash: `unzip oficinafacil.zip`
3. No console: `cd oficinafacil && pip install --user -r requirements.txt && python seed.py`
4. Em **Web → Add a new web app → Manual configuration (Python 3.x)**
5. No arquivo WSGI, deixe apenas:
   ```python
   import sys
   sys.path.insert(0, "/home/SEU_USUARIO/oficinafacil")
   from run import app as application
   ```
6. Em **Static files**, mapeie URL `/static/` para `/home/SEU_USUARIO/oficinafacil/app/views/static`
7. Clique em **Reload**. O sistema fica em `https://SEU_USUARIO.pythonanywhere.com`

(Alternativa: Render.com, com comando de start `gunicorn run:app`.)

---

## Manual de uso

**1. Acesso.** Na tela inicial, entre com e-mail e senha. Se for o primeiro acesso, clique em
*Cadastre-se* e crie o usuário (senha com no mínimo 6 caracteres).

**2. Painel.** Mostra o total de clientes e veículos, as ordens em aberto (agendadas ou em andamento),
o valor faturado com ordens concluídas e a agenda de serviços do dia.

**3. Clientes.** Menu *Clientes → + Novo cliente*. Nome e telefone são obrigatórios; CPF e e-mail são
opcionais. Use a busca para localizar por nome, telefone ou CPF. *Editar* altera os dados;
*Excluir* remove o cliente junto com os veículos e ordens dele (o sistema pede confirmação).

**4. Veículos.** Menu *Veículos → + Novo veículo*. Escolha o cliente proprietário e informe placa,
marca, modelo e ano. A placa é convertida para maiúsculas e validada (ABC1234 ou ABC1D23).
Não é possível cadastrar duas vezes a mesma placa.

**5. Ordens de serviço.** Menu *Ordens de serviço → + Nova ordem*. Selecione o veículo, descreva o
serviço, informe data/hora, valor e status. Na lista, use os botões de filtro para ver só um status
e altere o status direto pela caixa de seleção da linha: a mudança é salva na hora.

**6. Sair.** Clique em *Sair* no menu superior.

No celular, o menu fica no botão ☰ e as tabelas viram cartões.
