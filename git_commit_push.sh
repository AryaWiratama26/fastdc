#!/bin/bash

git add .

read -p "Masukkan pesan commit: " commit_message

git commit -m "$commit_message"

git push
