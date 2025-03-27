-- voir readme_pages/step_3__sql_requests_and_power_bi.md pour plus d'explications
UPDATE
    contrat
-- SET
--     salaire_min = NULL
--     , salaire_max = NULL;


SET
-------- ECRITURE DE LA COLONNE "SALAIRE_MIN"
salaire_min = CASE
-- pour 'cas 11 (annuel fourchette)' :
WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%' THEN
    CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
        NULL
        -- 11
    WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
    ELSE
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
    END
    -- pour 'cas 12 (annuel salaire unique)' :
WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
    OR "salaire_libelle" LIKE 'Annuel de % Euros' THEN
    CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
        NULL
        -- 12
    WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
    ELSE
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
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
END
-------- ECRITURE DE LA COLONNE "SALAIRE_MAX"
, salaire_max = CASE
-- pour 'cas 11 (annuel fourchette)' :
WHEN "salaire_libelle" LIKE 'Annuel de % Euros à % Euros%' THEN
    CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
        NULL
        -- 11
    WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER)
    ELSE
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)' , 1 , 2) AS INTEGER) * 12
    END
    -- pour 'cas 12 (annuel salaire unique)' :
WHEN "salaire_libelle" LIKE 'Annuel de % Euros sur%'
    OR "salaire_libelle" LIKE 'Annuel de % Euros' THEN
    CASE WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) < 20000 / 12 THEN
        NULL
        -- 12
    WHEN CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) > 20000 THEN
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER)
    ELSE
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') , '(\d+)') AS INTEGER) * 12
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
END
-- FROM
--     contrat
WHERE
    salaire_libelle IS NOT NULL
    AND salaire_libelle != 'Annuel de'
    AND salaire_libelle NOT LIKE 'Horaire %'
    AND alternance IS NOT TRUE


