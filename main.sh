#!/bin/sh
set -eu

cd "$(dirname "$0")"

# Generate the site before starting the web server.
python3 src/main.py

cd public
exec python3 -m http.server 8888
