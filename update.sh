#!/bin/bash
export RASPBERRY_PI=1
sudo systemctl stop kirby.service
mv database.db databasealt.db
git pull
mv databasealt.db database.db
sudo systemctl start kirby.service