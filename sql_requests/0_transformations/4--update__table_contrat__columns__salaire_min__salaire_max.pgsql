-- voir readme_pages/step_3__sql_requests_and_power_bi.md pour plus d'explications
-- reset des colonnes :
-- UPDATE
--     contrat
--     SET
--         salaire_min = NULL
--         , salaire_max = NULL;
WITH constante (
    seuil_salaire_mensuel_min
    , seuil_salaire_mensuel_max
    , seuil_salaire_annuel_min
    , seuil_salaire_annuel_max
) AS (
    VALUES (1666
            , 12500 --salaire mensuel ∈ [1 666, 12 500]
            , 20000
            , 150000) --salaire annuel ∈ [20 000, 150 000]
)
, salaire AS (
    SELECT
        salaire_libelle
        ,
        -- 1 AS get_salaire_min
        CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle
                    , '[.,]\d{1,2}'
                    , '') -- on supprime les . et les ,
                , '(\d+)') AS INTEGER) AS get_salaire_min
        , CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle
                    , '[.,]\d{1,2}'
                    , '') -- on supprime les . et les ,
                , '(\d+)'
                , 1
                , 2) AS INTEGER) AS get_salaire_max
    FROM
        contrat)
UPDATE
    contrat c
SET
    ------ ECRITURE DE LA COLONNE "SALAIRE_MIN" --------
    salaire_min = (
        CASE
        --
        -- pour 'cas fourchette' ---
        --
        WHEN c.salaire_libelle LIKE 'Annuel de % Euros à % Euros%'
            OR c.salaire_libelle LIKE 'Mensuel de % Euros à % Euros%'
            OR c.salaire_libelle LIKE 'De % Euros à % Euros%'
            OR c.salaire_libelle LIKE 'Autre de % Euros à % Euros'
            OR c.salaire_libelle LIKE 'Cachet de % Euros à % Euros' THEN
            CASE
            -- cas 1. Si salaire minimum récupéré > salaire maximal récupéré *ET* salaires min+max récupérés ∈ [1 600 €, 10 000 €] (on considère que c'est un salaire mensuel)
            --         alors on inverse les salaires mensuels minimum et maximum.
            WHEN get_salaire_min > get_salaire_max
                AND (get_salaire_min >= seuil_salaire_mensuel_min
                    AND get_salaire_min <= seuil_salaire_mensuel_max) THEN
                -- 1  -- pour investiguer
                get_salaire_max
                -- cas 2. Si salaires min+max récupérés ∈ [1 600 €, 10 000 €] (on considère que c'est un salaire mensuel)
                --         alors on récupère les salaires minimum et maximum et on les multiplie par 12.
            WHEN (get_salaire_min >= seuil_salaire_mensuel_min
                AND get_salaire_min <= seuil_salaire_mensuel_max)
                AND (get_salaire_max >= seuil_salaire_mensuel_min
                    AND get_salaire_max <= seuil_salaire_mensuel_max) THEN
                -- 2  -- pour investiguer
                get_salaire_min * 12
                -- cas 3. Si salaire minimum récupéré > salaire maximal récupéré *ET* salaires min+max récupérés ∈ [20 000 €, 200 000 €] (on considère que c'est un salaire annuel)
                --         alors on inverse les salaires annuels minimum et maximum.
            WHEN (get_salaire_min > get_salaire_max)
                AND (get_salaire_min >= seuil_salaire_annuel_min
                    AND get_salaire_min <= seuil_salaire_annuel_max)
                AND (get_salaire_max >= seuil_salaire_annuel_min
                    AND get_salaire_max <= seuil_salaire_annuel_max) THEN
                -- 3  -- pour investiguer
                get_salaire_max
                -- cas 4. Si salaires min+max récupérés ∈ [20 000 €, 200 000 €] (on considère que c'est un salaire annuel)
                -- alors on récupère les salaires minimum et maximum.
            WHEN (get_salaire_min >= seuil_salaire_annuel_min
                AND get_salaire_min <= seuil_salaire_annuel_max)
                AND (get_salaire_max >= seuil_salaire_annuel_min
                    AND get_salaire_max <= seuil_salaire_annuel_max) THEN
                -- 4  -- pour investiguer
                get_salaire_min
                ---
                --- pour 'cas salaire unique' ---
                ---
            END
        WHEN c.salaire_libelle LIKE 'Annuel de % Euros sur%'
            OR c.salaire_libelle LIKE 'Annuel de % Euros'
            OR c.salaire_libelle LIKE 'Mensuel de % Euros sur%'
            OR c.salaire_libelle LIKE 'Mensuel de % Euros' THEN
            CASE
            -- cas 2. Si salaire récupéré ∈ [1 600 €, 10 000 €] (on considère que c'est un salaire mensuel)
            --         alors on récupère le salaire et on le multiplie par 12.
            WHEN (get_salaire_min >= seuil_salaire_mensuel_min
                AND get_salaire_min <= seuil_salaire_mensuel_max) THEN
                -- 2  -- pour investiguer
                get_salaire_min * 12
                -- cas 4. Si salaire récupéré ∈ [20 000 €, 200 000 €] (on considère que c'est un salaire annuel)
                --         alors on récupère le salaire.
            WHEN (get_salaire_min >= seuil_salaire_annuel_min
                AND get_salaire_min <= seuil_salaire_annuel_max) THEN
                -- 4  -- pour investiguer
                get_salaire_min
            END
        END)
    ------ ECRITURE DE LA COLONNE "SALAIRE_MAX" --------
    , salaire_max = (
        CASE
        ---
        --- pour 'cas fourchette' ---
        ---
        WHEN c.salaire_libelle LIKE 'Annuel de % Euros à % Euros%'
            OR c.salaire_libelle LIKE 'Mensuel de % Euros à % Euros%'
            OR c.salaire_libelle LIKE 'De % Euros à % Euros%'
            OR c.salaire_libelle LIKE 'Autre de % Euros à % Euros'
            OR c.salaire_libelle LIKE 'Cachet de % Euros à % Euros' THEN
            CASE
            -- cas 1. Si salaire minimum récupéré > salaire maximal récupéré *ET* salaires min+max récupérés ∈ [1 600 €, 10 000 €] (on considère que c'est un salaire mensuel)
            --         alors on inverse les salaires mensuels minimum et maximum.
            WHEN get_salaire_min > get_salaire_max
                AND (get_salaire_min >= seuil_salaire_mensuel_min
                    AND get_salaire_min <= seuil_salaire_mensuel_max) THEN
                -- 1  -- pour investiguer
                get_salaire_min
                -- cas 2. Si salaires min+max récupérés ∈ [1 600 €, 10 000 €] (on considère que c'est un salaire mensuel)
                --         alors on récupère les salaires minimum et maximum et on les multiplie par 12.
            WHEN (get_salaire_min >= seuil_salaire_mensuel_min
                AND get_salaire_min <= seuil_salaire_mensuel_max)
                AND (get_salaire_max >= seuil_salaire_mensuel_min
                    AND get_salaire_max <= seuil_salaire_mensuel_max) THEN
                -- 2  -- pour investiguer
                get_salaire_max * 12
                -- cas 3. Si salaire minimum récupéré > salaire maximal récupéré *ET* salaires min+max récupérés ∈ [20 000 €, 200 000 €] (on considère que c'est un salaire annuel)
                --         alors on inverse les salaires annuels minimum et maximum.
            WHEN (get_salaire_min > get_salaire_max)
                AND (get_salaire_min >= seuil_salaire_annuel_min
                    AND get_salaire_min <= seuil_salaire_annuel_max)
                AND (get_salaire_max >= seuil_salaire_annuel_min
                    AND get_salaire_max <= seuil_salaire_annuel_max) THEN
                -- 3  -- pour investiguer
                get_salaire_min
                -- cas 4. Si salaires min+max récupérés ∈ [20 000 €, 200 000 €] (on considère que c'est un salaire annuel)
                -- alors on récupère les salaires minimum et maximum.
            WHEN (get_salaire_min >= seuil_salaire_annuel_min
                AND get_salaire_min <= seuil_salaire_annuel_max)
                AND (get_salaire_max >= seuil_salaire_annuel_min
                    AND get_salaire_max <= seuil_salaire_annuel_max) THEN
                -- 4  -- pour investiguer
                get_salaire_max
            END
            ---
            --- pour 'cas salaire unique' ---
            ---
        WHEN c.salaire_libelle LIKE 'Annuel de % Euros sur%'
            OR c.salaire_libelle LIKE 'Annuel de % Euros'
            OR c.salaire_libelle LIKE 'Mensuel de % Euros sur%'
            OR c.salaire_libelle LIKE 'Mensuel de % Euros' THEN
            CASE
            -- cas 2. Si salaire récupéré ∈ [1 600 €, 10 000 €] (on considère que c'est un salaire mensuel)
            --         alors on récupère le salaire et on le multiplie par 12.
            WHEN (get_salaire_min >= seuil_salaire_mensuel_min
                AND get_salaire_min <= seuil_salaire_mensuel_max) THEN
                -- 2  -- pour investiguer
                get_salaire_min * 12 -- c'est bien "get_salaire_min" car un salaire unique ici
                -- cas 4. Si salaire récupéré ∈ [20 000 €, 200 000 €] (on considère que c'est un salaire annuel)
                --         alors on récupère le salaire.
            WHEN (get_salaire_min >= seuil_salaire_annuel_min
                AND get_salaire_min <= seuil_salaire_annuel_max) THEN
                -- 4  -- pour investiguer
                get_salaire_min -- c'est bien "get_salaire_min" car un salaire unique ici
            END
        END)
FROM
    salaire s
    , constante
WHERE
    c.salaire_libelle = s.salaire_libelle
    AND c.salaire_libelle IS NOT NULL
    AND c.salaire_libelle != 'Annuel de'
    AND c.salaire_libelle NOT LIKE 'Horaire %'
    AND c.alternance IS NOT TRUE
