-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='2' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 2, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* we add "presence" access model */
ALTER TABLE nodes DROP CONSTRAINT nodes_access_model_check;
ALTER TABLE nodes ADD CHECK (access_model IN ('open', 'presence', 'publisher-roster', 'whitelist', 'publish-only', 'self-publisher'));

/* and schema column */
ALTER TABLE nodes ADD COLUMN schema xml;

/* we want xml types for items data too */
ALTER TABLE items ALTER data TYPE xml using data::xml;

UPDATE metadata SET value='3' WHERE key='version';
