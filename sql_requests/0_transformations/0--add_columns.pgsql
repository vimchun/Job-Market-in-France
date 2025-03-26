ALTER TABLE descriptionoffre
    ADD COLUMN "metier_data" VARCHAR(2);

ALTER TABLE contrat
    ADD COLUMN salaire_min INTEGER ,
    ADD COLUMN salaire_max INTEGER;

