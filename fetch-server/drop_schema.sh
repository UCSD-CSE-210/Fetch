#!/bin/bash

PSQL=psql

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <db name>" >&2
    exit 1
fi

DB="$1"

read -p "Drop db '$1'? " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PSQL postgres -c "DROP DATABASE IF EXISTS $1;" && \
        $PSQL postgres -c "CREATE DATABASE $1;" && \
        $PSQL postgres -c "GRANT ALL PRIVILEGES ON DATABASE $1 TO fetch_db;" && \
        $PSQL $1 -c "CREATE EXTENSION postgis;"
else
    echo "exiting..."
    exit 0
fi
