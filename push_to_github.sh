#!/bin/bash
# Push saved memes to GitHub
# Run after main.py
# Usage: ./push_to_github.sh

cd "$(dirname "$0")"
git add output/ seen_urls.txt
git commit -m "New memes $(date +'%Y-%m-%d %H:%M')"
git push origin main
echo "✅ Pushed to GitHub - Download from github.com/YOUR_USERNAME/YOUR_REPO/tree/main/output"
