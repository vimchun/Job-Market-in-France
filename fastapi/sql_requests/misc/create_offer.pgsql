-- === OffreEmploi
INSERT INTO OffreEmploi (
    offre_id,
    date_extraction,
    date_premiere_ecriture,
    date_creation,
    date_actualisation,
    nombre_postes
)
VALUES (
    %s,
    '2020-01-01',
    '2020-01-01',
    '2020-01-01',
    '2020-01-01',
1
);

-- === DescriptionOffre
INSERT INTO DescriptionOffre (
    offre_id,
    intitule_offre,
    description_offre,
    nom_partenaire,
    rome_code,
    rome_libelle,
    appellation_rome,
    difficile_a_pourvoir,
    accessible_travailleurs_handicapes,
    url_france_travail
)
VALUES (
    %s,
    'Offre factice pour FastAPI',
    'Description offre factice pour FastAPI',
    'Partenaire factice',
    'M1811',
    'Data engineer',
    'Data engineer',
    FALSE,
    TRUE,
    'url factice'
);

-- === Localisation
INSERT INTO Localisation (
    offre_id,
    code_insee,
    nom_commune,
    code_postal,
    nom_ville,
    code_departement,
    nom_departement,
    code_region,
    nom_region,
    lieu_cas
)
VALUES (
    %s,
    '75056',
    'Paris',
    '75000',
    'Paris',
    '75',
    'Paris',
    '11',
    'Île-de-France',
    'cas_1'
);

-- === Contrat de travail ===
INSERT INTO Contrat (
    offre_id,
    type_contrat,
    type_contrat_libelle,
    duree_travail_libelle,
    duree_travail_libelle_converti,
    nature_contrat,
    salaire_libelle,
    salaire_complement_1,
    salaire_complement_2,
    salaire_commentaire,
    alternance,
    deplacement_code,
    deplacement_libelle,
    temps_travail,
    condition_specifique
)
VALUES (
    %s,
    'CDI',
    'Contrat à durée indéterminée',
    'Temps plein',
    'Temps plein',
    'Contrat de travail',
    'Selon profil',
    'Autre',
    'Prime',
    'Selon grille de salaire convention',
    FALSE,
    NULL,
    NULL,
    'Temps plein',
    NULL
);
