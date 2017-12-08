#!/bin/bash

export FLASK_CONFIG_FILE=config.py 
export IMAGE_ROOT_FOLDER=$(readlink -f ../demo-images)

if ! [[ -d $IMAGE_ROOT_FOLDER          || \
        -d $IMAGE_ROOT_FOLDER/route    || \
        -d $IMAGE_ROOT_FOLDER/wildlife ]]; then
    echo "invalid images folder '$IMAGE_ROOT_FOLDER'" >&2
    exit 1
fi

python create_demo_db.py
