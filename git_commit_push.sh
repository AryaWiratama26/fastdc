#!/bin/bash

git add .

read -p "Commit Message: " commit_message

git commit -m "$commit_message"

git push
