#!/bin/bash

echo "Rebuilding site for production..."
jekyll build --config /workspace/eskimotv/_config.yml --source /workspace/eskimotv/app/ --destination /workspace/eskimotv/web
echo "Starting to ftp..."
lftp -u ${USERNAME},${PASSWORD} ${HOST} <<EOF
set ftp:ssl-allow false
mirror -R --parallel -c /workspace/eskimotv/web/ ./public_html
bye
EOF
echo "done"