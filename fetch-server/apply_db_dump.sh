#!/bin/bash

PSQL=psql

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <dump file>"
    exit 1
fi

if [[ ! -f $1 ]]; then
    echo "'$1' is not a regular file or missing"
    exit 1
fi

read -p "Drop db fetch_db? " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PSQL postgres -c "DROP DATABASE fetch_db;" && \
        $PSQL postgres -c "CREATE DATABASE fetch_db;" && \
        $PSQL postgres -c "GRANT ALL PRIVILEGES ON DATABASE fetch_db TO fetch_db;" && \
        $PSQL fetch_db -c "CREATE EXTENSION postgis;" && \
        $PSQL fetch_db < $1
else
    echo "exiting..."
    exit 0
fi
