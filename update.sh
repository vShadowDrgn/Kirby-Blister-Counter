#!/bin/bash
sudo systemctl stop kirby.service
mv database.db databasealt.db
git stash
git pull
mv databasealt.db database.db
sudo systemctl start kirby.service