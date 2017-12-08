#!/bin/bash

PSQL=psql
DB=fetch_db

if [[ $# -lt 2 ]]; then
	echo "usage: ${0:a:t} <lat> <long> [<dist> [where args...]]"
	exit 1
fi

LAT="$1"
LNG="$2"
shift
shift

ORDER_BY="ST_Distance(path, ST_GeogFromText('SRID=4326;POINT($LNG $LAT)'))"

if [[ $# -gt 0 ]]; then
	DIST="$1"
	shift
	WHERE="$ORDER_BY < 1609.34 * $DIST"

	if [[ $# -gt 0 ]]; then
		WHERE="$WHERE AND $@"
	fi

	SQL_QUERY="SELECT name FROM route WHERE $WHERE ORDER BY $ORDER_BY ASC;"
else
	SQL_QUERY="SELECT name FROM route ORDER BY $ORDER_BY ASC;"
fi

echo "$SQL_QUERY"
echo

$PSQL $DB -c "$SQL_QUERY"
