-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='4' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 4, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* new "max_items" and "consistent publisher" options */
ALTER TABLE nodes ADD COLUMN max_items integer NOT NULL DEFAULT 0
		CHECK (max_items >= 0);
ALTER TABLE nodes ADD COLUMN consistent_publisher boolean NOT NULL DEFAULT FALSE;

UPDATE metadata SET value='5' WHERE key='version';
