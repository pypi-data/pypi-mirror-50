-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF FOUND THEN
        RAISE EXCEPTION 'This update file needs to be applied on older database, you don''t have to use it';
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check


ALTER TABLE nodes ADD COLUMN pep text;

ALTER TABLE nodes DROP CONSTRAINT nodes_node_key;
/* we need 2 partial indexes to manage NULL value for PEP */
CREATE UNIQUE INDEX nodes_node_pep_key_not_null ON nodes(node, pep) WHERE pep IS NOT NULL;
CREATE UNIQUE INDEX nodes_node_pep_key_null ON nodes(node) WHERE pep IS NULL;

CREATE TABLE metadata (
	key text PRIMARY KEY,
	value text
);

INSERT INTO metadata VALUES ('version', '1');

CREATE TABLE item_categories (
    item_categories_id serial PRIMARY KEY,
    item_id integer NOT NULL references items ON DELETE CASCADE,
    category text NOT NULL,
    UNIQUE (item_id,category)
);

UPDATE nodes SET node='urn:xmpp:microblog:0', pep=substring(node from 20) WHERE node LIKE 'urn:xmpp:groupblog:_%';

/* This is to update namespaces, SàT was buggy before 0.6 and didn't set the atom namespace in <entry/> */
/* But yeah, this is a crazy query */
UPDATE items SET data = xmlelement(name item, xmlattributes((xpath('/item/@id', data::xml))[1] as id),
                        XMLPARSE(CONTENT NULLIF(array_to_string(xpath('/item/entry/preceding-sibling::*', data::xml)::text[],''),'')),
                        xmlelement(name entry, xmlattributes('http://www.w3.org/2005/Atom' as xmlns), array_to_string(xpath('/item/entry/*', data::xml)::text[], '')::xml),
                        XMLPARSE(CONTENT NULLIF(array_to_string(xpath('/item/entry/following-sibling::*', data::xml)::text[],''),'')))
             FROM nodes WHERE nodes.node_id = items.node_id
             AND (node = 'urn:xmpp:microblog:0' or node LIKE 'urn:xmpp:comments:%')
             AND XMLEXISTS('/item/entry' PASSING (data::xml));
