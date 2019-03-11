#!/bin/bash

echo "Rebuilding site for production..."
jekyll build --config /workspace/critical-truth/_config.yml --source /workspace/critical-truth/app/ --destination /workspace/critical-truth/web
echo "Starting to ftp..."
lftp -u ${USER},${PASS} ${HOST} <<EOF
set ftp:ssl-allow false
mirror -R --parallel -c /workspace/critical-truth/web/ ./public_html
bye
EOF
echo "done"