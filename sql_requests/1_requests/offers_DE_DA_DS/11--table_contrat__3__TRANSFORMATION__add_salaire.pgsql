-- voir readme_pages/step_3__sql_requests_and_power_bi.md pour plus d'explications


SELECT
    salaire_libelle
    , CASE
    -------- ECRITURE DE LA COLONNE "CAS"
    -- pour 'cas 11 (annuel fourchette)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%' THEN
        'cas 11 (annuel fourchette)'
        -- pour 'cas 12 (annuel salaire unique)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Annuel de % Euros' THEN
        'cas 12 (annuel salaire unique)'
        -- pour 'cas 21 (mensuel fourchette)'
    WHEN "salaire_libelle" LIKE 'Mensuel de % Euros à % Euros%' THEN
        'cas 21 (mensuel fourchette)'
        -- pour 'cas 22 (mensuel salaire unique)'
    WHEN "salaire_libelle" LIKE 'Mensuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros' THEN
        'cas 22 (mensuel salaire unique)'
        -- pour 'cas 31 (fourchette mensuelle ou annuelle ?)'
    WHEN "salaire_libelle" LIKE 'De % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Autre de % Euros à % Euros'
        OR "salaire_libelle" LIKE 'Cachet de % Euros à % Euros' THEN
        'cas 31 (mensuel ou annuel ?)'
    END AS cas
    -- -------- ECRITURE DE LA COLONNE "SALAIRE_MIN"
    , CASE
    -- pour 'cas 11 (annuel fourchette)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 THEN
            NULL
            -- 11
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        END
        -- pour 'cas 12 (annuel salaire unique)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Annuel de % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 THEN
            NULL
            -- 12
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        END
        -- pour 'cas 21 (mensuel fourchette)'
    WHEN "salaire_libelle" LIKE 'Mensuel de % Euros à % Euros%' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 21
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
        END
        -- pour 'cas 22 (mensuel salaire unique)'
    WHEN "salaire_libelle" LIKE 'Mensuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 22
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
        END
        -- pour 'cas 31 (fourchette mensuelle ou annuelle ?)'
    WHEN "salaire_libelle" LIKE 'De % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Autre de % Euros à % Euros'
        OR "salaire_libelle" LIKE 'Cachet de % Euros à % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 31
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
        END
    END AS salaire_min
    -------- ECRITURE DE LA COLONNE "SALAIRE_MAX"
    , CASE
    -- pour 'cas 11 (annuel fourchette)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 THEN
            NULL
            -- 11
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
        END
        -- pour 'cas 12 (annuel salaire unique)' :
    WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Annuel de % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 THEN
            NULL
            -- 12
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        END
        -- pour 'cas 21 (mensuel fourchette)'
    WHEN "salaire_libelle" LIKE 'Mensuel de % Euros à % Euros%' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 21
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) * 12
        END
        -- pour 'cas 22 (mensuel salaire unique)'
    WHEN "salaire_libelle" LIKE 'Mensuel de % Euros sur%'
        OR "salaire_libelle" LIKE 'Mensuel de % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 22
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
        END
        -- pour 'cas 31 (fourchette mensuelle ou annuelle ?)'
    WHEN "salaire_libelle" LIKE 'De % Euros à % Euros%'
        OR "salaire_libelle" LIKE 'Autre de % Euros à % Euros'
        OR "salaire_libelle" LIKE 'Cachet de % Euros à % Euros' THEN
        CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
            NULL
            -- 31
        WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
        ELSE
            CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) * 12
        END
    END AS salaire_max
FROM
    contrat
WHERE
    salaire_libelle IS NOT NULL
    AND salaire_libelle != 'Annuel de'
    AND salaire_libelle NOT LIKE 'Horaire %'
ORDER BY
    cas ASC
    , salaire_min ASC
