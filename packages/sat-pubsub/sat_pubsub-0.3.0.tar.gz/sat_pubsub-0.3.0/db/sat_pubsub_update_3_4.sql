-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='3' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 3, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* new "serial ids" option */
ALTER TABLE nodes ADD COLUMN serial_ids boolean NOT NULL DEFAULT FALSE;

/* we want to keep creation and update times */
ALTER TABLE items RENAME COLUMN date TO created;
ALTER TABLE items ADD COLUMN updated timestamp with time zone NOT NULL DEFAULT now();

UPDATE metadata SET value='4' WHERE key='version';
