python3 src/main.py "/static-site-generator/"


USER=$(gh api user --jq '.login')
REPO=$(basename "$(git rev-parse --show-toplevel)")
URL="https://github.com/$USER/$REPO"

echo "$URL"
