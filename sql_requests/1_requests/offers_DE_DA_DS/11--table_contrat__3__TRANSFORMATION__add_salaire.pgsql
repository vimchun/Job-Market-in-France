-- voir readme_pages/step_3__sql_requests_and_power_bi.md pour plus d'explications
SELECT
    intitule_offre
    , salaire_libelle
    , alternance
    , CASE
    -------- ECRITURE DE LA COLONNE "CAS"
    -- pour 'cas 1 (fourchette)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'De % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Autre de % Euros à % Euros'
        OR "salaire_libelle" LIKE 'Cachet de % Euros à % Euros' THEN
        'cas 1 (fourchette)'
        -- pour 'cas 2 (salaire unique)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Annuel de % Euros'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros' THEN
        'cas 2 (salaire unique)'
    END AS cas
    -- -------- ECRITURE DE LA COLONNE "SALAIRE_MIN"
    , CASE WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'De % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Autre de % Euros à % Euros'
        OR "salaire_libelle" LIKE 'Cachet de % Euros à % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) > 200000
            OR CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12
            OR (CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
                AND CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) > 200000) THEN
            NULL
            -- 1
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
            AND CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) < 200000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) >= 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
        END
        -- pour 'cas 2 (salaire unique)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Annuel de % Euros'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 200000
            OR CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 2
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) >= 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
        END
    END AS salaire_min
    -------- ECRITURE DE LA COLONNE "SALAIRE_MAX"
    , CASE WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'De % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Autre de % Euros à % Euros'
        OR "salaire_libelle" LIKE 'Cachet de % Euros à % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) > 200000
            OR CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12
            OR (CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
                AND CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) > 200000) THEN
            NULL
            -- 1
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
            AND CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) < 200000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) >= 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) * 12
        END
        -- pour 'cas 2 (salaire unique)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Annuel de % Euros'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 200000 or CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 2
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) >= 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
        END
    END AS salaire_max
FROM
    contrat c
    JOIN descriptionoffre dof ON dof.offre_id = c.offre_id
WHERE
    salaire_libelle IS NOT NULL
        AND salaire_libelle != 'Annuel de'
        AND salaire_libelle NOT LIKE 'Horaire %'
        AND alternance IS NOT TRUE
    ORDER BY
        -- cas ASC
        salaire_min DESC
        , salaire_max DESC;

