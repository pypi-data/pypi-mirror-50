-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver smallint;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='1' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 1, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* roster access model was badly used, we rename it to publisher-roster */

ALTER TABLE nodes DROP CONSTRAINT nodes_access_model_check;
UPDATE nodes SET access_model = 'publisher-roster' WHERE access_model = 'roster';
ALTER TABLE nodes ADD CHECK (access_model IN ('open', 'publisher-roster', 'whitelist', 'publish-only', 'self-publisher'));

ALTER TABLE items DROP CONSTRAINT items_access_model_check;
UPDATE items SET access_model = 'publisher-roster' WHERE access_model = 'roster';
ALTER TABLE items ADD CHECK (access_model IN ('open', 'publisher-roster', 'whitelist'));

ALTER TABLE affiliations DROP CONSTRAINT affiliations_affiliation_check;
ALTER TABLE affiliations ADD CHECK (affiliation IN ('outcast', 'member', 'publisher', 'owner'));

CREATE TABLE item_jids_authorized (
    item_jids_authorized_id serial PRIMARY KEY,
    item_id integer NOT NULL references items ON DELETE CASCADE,
    jid text NOT NULL,
    UNIQUE (item_id,jid)
);

CREATE TABLE item_languages (
    item_languages_id serial PRIMARY KEY,
    item_id integer NOT NULL references items ON DELETE CASCADE,
    language text NOT NULL,
    UNIQUE (item_id,language)
);

UPDATE metadata SET value='2' WHERE key='version';
