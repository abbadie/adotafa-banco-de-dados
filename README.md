# AdotaFá - Sistema de Adoção Responsável

Projeto individual desenvolvido por **Davi Noronha da Matta Baptista** para a disciplina **Banco de Dados**, semestre 2026/2, orientada pelo professor Howard Roatti. A aplicação de console gerencia adotantes, animais e adoções, utilizando Python e PostgreSQL sem ORM.

## Funcionalidades

- Splash screen com identificação do autor e contagem dos registros das três tabelas.
- Inclusão, atualização e remoção de adotantes, animais e adoções.
- Tratamento das chaves estrangeiras antes da remoção de adotantes e animais.
- Relatório de adoções agrupadas por espécie (`GROUP BY`, `COUNT`, `SUM` e `AVG`).
- Relatório detalhado de adoções com junção das três tabelas (`INNER JOIN`).
- Menus persistentes, confirmações e validação das entradas.

## Modelo relacional

O sistema utiliza três entidades:

- `ADOTANTES`: pessoas cadastradas para realizar adoções.
- `ANIMAIS`: animais acolhidos e seu estado no processo de adoção.
- `ADOCOES`: associa um adotante a um animal e registra a data e a taxa da adoção.

Cardinalidades:

- Um adotante pode realizar nenhuma ou várias adoções.
- Um animal pode participar de nenhuma ou uma adoção.
- Toda adoção deve possuir exatamente um adotante e um animal.

Os arquivos prontos para entrega estão em [diagrama/diagrama_relacional.pdf](diagrama/diagrama_relacional.pdf) e [diagrama/diagrama_relacional.png](diagrama/diagrama_relacional.png). O código Mermaid editável fica em [diagrama/diagrama_relacional.mmd](diagrama/diagrama_relacional.mmd).

## Pré-requisitos no Linux

- Ubuntu 22.04 ou distribuição equivalente.
- Python 3.10 ou superior.
- PostgreSQL 14 ou superior.
- Acesso a um usuário capaz de criar banco de dados.

## Instalação no Linux

No terminal, entre na pasta do projeto e execute:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip postgresql postgresql-client

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Crie o banco e um usuário exclusivo. Os nomes abaixo podem ser alterados, desde que as variáveis de ambiente usem os mesmos valores:

```bash
sudo -u postgres psql
```

Dentro do `psql`:

```sql
CREATE USER adotafa_app WITH PASSWORD 'troque_esta_senha';
CREATE DATABASE adotafa OWNER adotafa_app ENCODING 'UTF8';
\q
```

Crie as tabelas e a carga inicial:

```bash
psql -h localhost -U adotafa_app -d adotafa -f sql/01_criacao_tabelas.sql
psql -h localhost -U adotafa_app -d adotafa -f sql/02_carga_inicial.sql
```

## Configuração

Copie o arquivo de exemplo e proteja sua senha. O arquivo `.env` não é lido automaticamente; ele serve como referência para exportar as variáveis no terminal.

```bash
cp .env.example .env
chmod 600 .env
set -a
source .env
set +a
```

O arquivo local `.env` deve manter `INTEGRANTES="Davi Noronha da Matta Baptista"`. As aspas permitem carregar o nome com espaços no terminal Linux. A splash screen utiliza essa variável. Esse arquivo contém a senha local e, por segurança, não deve ser enviado ao GitHub.

## Execução

Com o ambiente virtual ativo e as variáveis carregadas:

```bash
python -m src.principal
```

O programa testa a conexão, apresenta a splash screen, informa a quantidade de registros e mantém o menu principal visível até a opção de saída.

## Testes

Os testes unitários não alteram o banco de dados:

```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

Existe também um teste opcional de ponta a ponta que cria e remove registros temporários no banco de desenvolvimento configurado:

```bash
RUN_DB_TESTS=1 python -m unittest tests.test_integracao_postgresql -v
```

Para uma verificação manual completa, use a ordem sugerida:

1. Cadastre um adotante.
2. Cadastre um animal.
3. Registre a adoção e observe a mudança do animal para `ADOTADO`.
4. Execute os dois relatórios.
5. Atualize um registro.
6. Tente remover um adotante ou animal referenciado e teste a confirmação de exclusão da adoção dependente.

## Estrutura do projeto

```text
.
|-- diagrama/                # Modelo relacional em Mermaid, PNG e PDF
|-- docs/                    # Roteiro do vídeo e checklist de entrega
|-- sql/                     # Criação das tabelas e carga inicial
|-- src/
|   |-- conexao/             # Abertura da conexão PostgreSQL
|   |-- controller/          # CRUD e regras de integridade
|   |-- model/               # Classes das entidades
|   |-- reports/             # Execução dos relatórios
|   |-- sql/                 # Consultas SQL dos relatórios
|   |-- utils/               # Configuração, entrada, tabela e splash
|   `-- principal.py         # Menus e fluxo da aplicação
|-- tests/                   # Testes automatizados
|-- PROMPTS.md               # Transparência sobre o uso de IA
`-- requirements.txt         # Dependência do projeto
```

## Entrega e vídeo

- Revise [docs/CHECKLIST_ENTREGA.md](docs/CHECKLIST_ENTREGA.md).
- O vídeo demonstrativo apresenta a execução real do programa, conforme a sequência em [docs/ROTEIRO_VIDEO.md](docs/ROTEIRO_VIDEO.md).
- Adicione `howardroatti` como colaborador do repositório.
- Por ser um projeto individual, todos os commits e a apresentação devem ser realizados por Davi Noronha da Matta Baptista.
- Consulte [PROMPTS.md](PROMPTS.md) para o registro transparente do uso de inteligência artificial no desenvolvimento e na narração do vídeo.
- No AVA, envie somente o link do repositório (ou um `.txt` com o link, se o sistema exigir um arquivo).

**Repositório:** [abbadie/adotafa-banco-de-dados](https://github.com/abbadie/adotafa-banco-de-dados).

**Link do vídeo:** [Demonstração do AdotaFá no YouTube](https://youtu.be/pBHH4sSRwMs).

## Autor

**Davi Noronha da Matta Baptista**. O nome também é lido da variável `INTEGRANTES` para ser exibido na splash screen.

