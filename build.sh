python3 src/main.py "/static-site-generator/"


USER=$(gh api user --jq '.login')
REPO=$(basename "$(git rev-parse --show-toplevel)")
URL="https://${USER}.github.io/${REPO}/"
URL_REPO="https://github.com/$USER/$REPO"

echo "$URL"
echo "$URL_REPO"
