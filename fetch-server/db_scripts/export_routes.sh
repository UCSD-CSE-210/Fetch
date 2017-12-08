#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "usage: ${0:a:t} <json file>" >&2
    exit 1
fi

PSQL=psql
DB=fetch_db
OUT="$1"

TMP=$(mktemp "${OUT}.XXXXXX")

$PSQL $DB -c 'COPY (SELECT ROW_TO_JSON(t) FROM (SELECT *, ST_AsText(path) as path_str FROM route) t) TO '"'"$TMP"';"

echo '[' > $OUT
paste -s -d, $TMP >> $OUT
echo ']' >> $OUT

rm -f $TMP
