#!/bin/bash
########################################################################
# Remove git history 
# Use case is when updating github pages, do not want to retain old info
#########################################################################
GITREMOTE=
GITCOMMENT='Commit to publish'

rm -rf .git
git init
git remote add origin $GITREMOTE
git add .
git commit -m "$GITCOMMENT"
git push -u --force origin master
