-- AdotaFá - criação do modelo relacional em PostgreSQL
-- Disciplina: Banco de Dados - semestre 2026/2

BEGIN;

CREATE TABLE IF NOT EXISTS adotantes (
    id_adotante INTEGER GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL,
    cidade VARCHAR(80) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_adotantes PRIMARY KEY (id_adotante),
    CONSTRAINT uq_adotantes_cpf UNIQUE (cpf),
    CONSTRAINT uq_adotantes_email UNIQUE (email),
    CONSTRAINT ck_adotantes_cpf CHECK (cpf ~ '^[0-9]{11}$'),
    CONSTRAINT ck_adotantes_nome CHECK (char_length(trim(nome)) >= 3)
);

CREATE TABLE IF NOT EXISTS animais (
    id_animal INTEGER GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(80) NOT NULL,
    especie VARCHAR(10) NOT NULL,
    sexo CHAR(1) NOT NULL,
    idade_aproximada SMALLINT NOT NULL,
    porte VARCHAR(7) NOT NULL,
    status_adocao VARCHAR(12) NOT NULL DEFAULT 'DISPONIVEL',
    data_entrada DATE NOT NULL,
    CONSTRAINT pk_animais PRIMARY KEY (id_animal),
    CONSTRAINT ck_animais_especie CHECK (especie IN ('CACHORRO', 'GATO', 'OUTRO')),
    CONSTRAINT ck_animais_sexo CHECK (sexo IN ('M', 'F')),
    CONSTRAINT ck_animais_idade CHECK (idade_aproximada BETWEEN 0 AND 35),
    CONSTRAINT ck_animais_porte CHECK (porte IN ('PEQUENO', 'MEDIO', 'GRANDE')),
    CONSTRAINT ck_animais_status CHECK (
        status_adocao IN ('DISPONIVEL', 'ADOTADO', 'INDISPONIVEL')
    ),
    CONSTRAINT ck_animais_data CHECK (data_entrada <= CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS adocoes (
    id_adocao INTEGER GENERATED ALWAYS AS IDENTITY,
    id_adotante INTEGER NOT NULL,
    id_animal INTEGER NOT NULL,
    data_adocao DATE NOT NULL,
    taxa NUMERIC(10, 2) NOT NULL DEFAULT 0,
    observacoes VARCHAR(300),
    CONSTRAINT pk_adocoes PRIMARY KEY (id_adocao),
    CONSTRAINT fk_adocoes_adotantes FOREIGN KEY (id_adotante)
        REFERENCES adotantes (id_adotante)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_adocoes_animais FOREIGN KEY (id_animal)
        REFERENCES animais (id_animal)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT uq_adocoes_animal UNIQUE (id_animal),
    CONSTRAINT ck_adocoes_data CHECK (data_adocao <= CURRENT_DATE),
    CONSTRAINT ck_adocoes_taxa CHECK (taxa >= 0)
);

CREATE INDEX IF NOT EXISTS ix_adocoes_adotante ON adocoes (id_adotante);
CREATE INDEX IF NOT EXISTS ix_animais_status ON animais (status_adocao);

COMMIT;

