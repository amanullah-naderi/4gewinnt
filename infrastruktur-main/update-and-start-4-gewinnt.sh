#! /bin/bash

git submodule update --init --remote

docker compose up -d --build --force-recreate
