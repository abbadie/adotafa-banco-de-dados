SELECT
    adocao.id_adocao AS "Código",
    TO_CHAR(adocao.data_adocao, 'DD/MM/YYYY') AS "Data",
    animal.nome AS "Animal",
    animal.especie AS "Espécie",
    adotante.nome AS "Adotante",
    adotante.cidade AS "Cidade",
    adocao.taxa AS "Taxa (R$)"
FROM adocoes AS adocao
INNER JOIN animais AS animal ON animal.id_animal = adocao.id_animal
INNER JOIN adotantes AS adotante ON adotante.id_adotante = adocao.id_adotante
ORDER BY adocao.data_adocao DESC, adocao.id_adocao DESC;

