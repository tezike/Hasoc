#!/bin/bash

echo "Username, Email and Password must be set as env-vars using 'USERNAME' and 'EMAIL', 'PASSWORD' "
git config --global user.email $EMAIL
git config --global user.name $USERNAME
git init
git remote rm origin
git remote add origin https://$USERNAME:$PASSWORD@github.com/$USERNAME/${PWD##*/}.git
git pull origin master --allow-unrelated-histories

# Make jupyter terminal show branch name
# git_branch() {
#   git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
# }
# export PS1="[\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w\$(git_branch)\$ "

echo "git_branch() {" >> ~/.bashrc
echo "      git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'" >> ~/.bashrc
echo "    }" >> ~/.bashrc
echo 'export PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w\$ (git_branch)\$ "' >> ~/.bashrc

# in the terminal, type
# source ~/.bashrc