#!/bin/bash
cd /var/www/vhosts/edefrutos2025.xyz/httpdocs
source .venv/bin/activate
gunicorn --workers 3 --bind 127.0.0.1:8000 app:app
