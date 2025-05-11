SELECT
    intitule_offre
FROM
    descriptionoffre dof
WHERE
    rome_code = 'M1811';
    -- "rome_code = M1811" correspond à "rome_libelle = Data engineer",
    --   mais ce n'est pas pour autant que ce sont des offres DE...
    --    (voir résultat de la requête)
