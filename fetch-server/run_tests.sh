#!/bin/bash

DB='fetch_db_test'
CONF='test_config.py'

export FLASK_CONFIG_FILE=$CONF

(echo 'y' | ./drop_schema.sh $DB) && \
    python create_test_db.py && \
    python test.py
