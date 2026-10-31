-- Dados fictícios para demonstração do AdotaFá.
-- O bloco só insere os registros quando as tabelas estão vazias.

BEGIN;

INSERT INTO adotantes (nome, cpf, telefone, email, cidade, ativo)
SELECT dados.nome, dados.cpf, dados.telefone, dados.email, dados.cidade, dados.ativo
FROM (
    VALUES
        ('Marina Alves', '12345678901', '(27) 99911-2233', 'marina.alves@example.com', 'Vitória', TRUE),
        ('Rafael Costa', '23456789012', '(27) 99822-3344', 'rafael.costa@example.com', 'Serra', TRUE),
        ('Beatriz Lima', '34567890123', '(27) 99733-4455', 'beatriz.lima@example.com', 'Vila Velha', TRUE)
) AS dados(nome, cpf, telefone, email, cidade, ativo)
WHERE NOT EXISTS (SELECT 1 FROM adotantes);

INSERT INTO animais (
    nome, especie, sexo, idade_aproximada, porte, status_adocao, data_entrada
)
SELECT dados.nome, dados.especie, dados.sexo, dados.idade, dados.porte,
       dados.status_adocao, dados.data_entrada
FROM (
    VALUES
        ('Luna', 'GATO', 'F', 2, 'PEQUENO', 'ADOTADO', DATE '2026-07-10'),
        ('Tobias', 'CACHORRO', 'M', 4, 'MEDIO', 'DISPONIVEL', DATE '2026-08-03'),
        ('Mel', 'CACHORRO', 'F', 1, 'PEQUENO', 'ADOTADO', DATE '2026-08-19'),
        ('Nino', 'GATO', 'M', 3, 'PEQUENO', 'DISPONIVEL', DATE '2026-09-02'),
        ('Jade', 'OUTRO', 'F', 2, 'PEQUENO', 'INDISPONIVEL', DATE '2026-09-15')
) AS dados(nome, especie, sexo, idade, porte, status_adocao, data_entrada)
WHERE NOT EXISTS (SELECT 1 FROM animais);

INSERT INTO adocoes (id_adotante, id_animal, data_adocao, taxa, observacoes)
SELECT adotante.id_adotante, animal.id_animal, dados.data_adocao,
       dados.taxa, dados.observacoes
FROM (
    VALUES
        ('12345678901', 'Luna', DATE '2026-08-20', 60.00, 'Acompanhamento realizado após 30 dias.'),
        ('23456789012', 'Mel', DATE '2026-09-12', 80.00, 'Família possui quintal protegido.')
) AS dados(cpf, nome_animal, data_adocao, taxa, observacoes)
INNER JOIN adotantes AS adotante ON adotante.cpf = dados.cpf
INNER JOIN animais AS animal ON animal.nome = dados.nome_animal
WHERE NOT EXISTS (SELECT 1 FROM adocoes);

COMMIT;

