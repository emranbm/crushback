#!/bin/bash
set -eu

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${CRUSHBACK_DB_USER} WITH ENCRYPTED PASSWORD '${CRUSHBACK_DB_PASSWORD}';
    CREATE DATABASE ${CRUSHBACK_DB_NAME};
    \connect ${CRUSHBACK_DB_NAME};
    CREATE SCHEMA ${CRUSHBACK_DB_SCHEMA} AUTHORIZATION ${CRUSHBACK_DB_USER};
    ALTER ROLE ${CRUSHBACK_DB_USER} SET client_encoding TO 'utf8';
    ALTER ROLE ${CRUSHBACK_DB_USER} SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ${CRUSHBACK_DB_USER} SET timezone TO 'UTC';
EOSQL
