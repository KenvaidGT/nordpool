#!/bin/bash
set -e

echo "Deploy started"

cd /home/deploy/nordpool

git fetch origin
git reset --hard origin/main
git clean -fd

docker compose pull
docker compose up -d --build

echo "Deploy finished"