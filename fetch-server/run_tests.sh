#!/bin/bash

DB='fetch_db_test'
CONF='test_config.py'

export FLASK_CONFIG_FILE=$CONF

if [[ $# -eq 0 ]]; then
    (echo 'y' | ./drop_schema.sh $DB) && \
        python create_test_db.py && \
        python test.py
elif [[ $# -eq 1 ]]; then
    if [[ ! -f test/test_$1.py ]]; then
        echo "'test/test_$1.py' does not exist" >&2
        exit 1
    fi
        
    (echo 'y' | ./drop_schema.sh $DB) && \
        python create_test_db.py && \
        python -m unittest test.test_$1
else
    echo "usage: ${0:a:t} [<test file suffix>]" >&2
    echo "       suffix is extended into test/test_*.py" >&2
    exit 1
fi
