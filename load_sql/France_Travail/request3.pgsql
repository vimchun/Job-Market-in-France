SELECT
    o.id
    , o.intitule
    , l.codePostal
FROM
    offre o
    JOIN localisation l ON o.id = l.id
WHERE
    o.id = '186NWKN';