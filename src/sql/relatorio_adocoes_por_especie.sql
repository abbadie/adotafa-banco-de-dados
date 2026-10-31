SELECT
    animal.especie AS "Espécie",
    COUNT(adocao.id_adocao) AS "Quantidade de adoções",
    COALESCE(SUM(adocao.taxa), 0) AS "Total de taxas (R$)",
    COALESCE(ROUND(AVG(adocao.taxa), 2), 0) AS "Taxa média (R$)"
FROM animais AS animal
LEFT JOIN adocoes AS adocao ON adocao.id_animal = animal.id_animal
GROUP BY animal.especie
ORDER BY COUNT(adocao.id_adocao) DESC, animal.especie;

