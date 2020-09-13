#!/bin/bash

echo "Username, Email and Password must be set as env-vars using 'USERNAME' and 'EMAIL', 'PASSWORD' "
git config --global user.email $EMAIL
git config --global user.name $USERNAME
git init
git remote rm origin
git remote add origin https://$USERNAME:$PASSWORD@github.com/$USERNAME/${PWD##*/}.git
git pull origin master --allow-unrelated-histories
