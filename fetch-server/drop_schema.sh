#!/bin/bash

PSQL=psql

read -p "Drop db fetch_db? " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PSQL postgres -c "DROP DATABASE fetch_db;" && \
        $PSQL postgres -c "CREATE DATABASE fetch_db;" && \
        $PSQL postgres -c "GRANT ALL PRIVILEGES ON DATABASE fetch_db TO fetch_db;" && \
        $PSQL fetch_db -c "CREATE EXTENSION postgis;"
else
    echo "exiting..."
    exit 0
fi
