SELECT
    COUNT(l.langue_libelle) AS nombre_occurences
    , l.langue_libelle
    , l.langue_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_langue ol ON ol.offre_id = dof.offre_id
    JOIN langue l ON ol.langue_id = l.langue_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    l.langue_libelle
    , l.langue_code_exigence
ORDER BY
    --tri par E(xigé), S(ouhaité)
    langue_code_exigence ASC
    , langue_libelle ASC;

