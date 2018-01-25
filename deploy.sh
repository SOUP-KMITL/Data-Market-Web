#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]
then
    echo "rsync -azrP --exclude-from \"rsync.exc\" --include \".dockerignore\" \
        ./ api-smartCity:/home/centos/kohpai/WebService/"
    rsync -azrP --exclude-from "rsync.exc" --include ".dockerignore" \
        ./ api-smartCity:/home/centos/kohpai/WebService/
else
    echo "rsync -azrP --exclude-from \"rsync.exc\" --include \".dockerignore\" ./ $1:$2"
    rsync -azrP --exclude-from "rsync.exc" --include ".dockerignore" ./ $1:$2
fi

