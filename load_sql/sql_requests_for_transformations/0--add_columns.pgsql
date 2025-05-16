ALTER TABLE descriptionoffre
    ADD COLUMN IF NOT EXISTS metier_data VARCHAR(2) ,
    ADD COLUMN IF NOT EXISTS liste_mots_cles TEXT[]; -- liste
--  ADD COLUMN IF NOT EXISTS occurence_mots_cles JSONB;

ALTER TABLE contrat
    ADD COLUMN IF NOT EXISTS salaire_min INTEGER ,
    ADD COLUMN IF NOT EXISTS salaire_max INTEGER;
