#!/bin/bash

# 1. Run the update script first so the new data is generated
echo "📊 Updating dashboard data..."
python3 update_dashboard.py

# Check if the python script failed
if [ $? -ne 0 ]; then
    echo "❌ Python script failed! Aborting push."
    exit 1
fi

# 2. Add changes to git
echo "➕ Staging changes..."
git add .

# 3. Commit with the current date and time automatically
DATE=$(date +"%Y-%m-%d %H:%M")
echo "📝 Committing changes..."
git commit -m "Updated dashboard: $DATE"

# 4. Push to GitHub
echo "🚀 Pushing to GitHub..."
git push

echo "✅ Done! Your dashboard is live."