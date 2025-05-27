SELECT
    REGEXP_MATCHES('Il faut connaitre de Python, R, SQL' , '(?<![a-zA-Z0-9_])r(?![a-zA-Z0-9_])' , 'gi');
-- regex insensible (flag i) :
--   - Avant le r, il ne faut pas de lettre, chiffre ou _ ([a-zA-Z0-9_])
--   - Après le r, idem
