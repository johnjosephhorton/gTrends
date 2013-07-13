BEGIN TRANSACTION;
CREATE TABLE meta_data (group_id NUMERIC, launched TEXT, pk_id INTEGER PRIMARY KEY, query_string TEXT, url TEXT);
CREATE TABLE search_term_groups (id NUMERIC, pk_id INTEGER PRIMARY KEY, term TEXT);
CREATE TABLE search_volume (pk_id INTEGER PRIMARY KEY, group_id NUMERIC, term TEXT, time_period_end TEXT, time_period_start TEXT, volume NUMERIC);
COMMIT;
