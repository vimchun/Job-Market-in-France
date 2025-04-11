ALTER TABLE descriptionoffre
    ADD COLUMN metier_data VARCHAR(2) ,
    ADD COLUMN liste_mots_cles TEXT[];  -- liste
    -- ADD COLUMN occurence_mots_cles JSONB;

ALTER TABLE contrat
    ADD COLUMN salaire_min INTEGER ,
    ADD COLUMN salaire_max INTEGER;

