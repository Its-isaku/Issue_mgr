#!/bin/bash

# Deploy script for Heroku
echo "🚀 Deploying Issue Manager to Heroku..."

# Make sure we're in the right directory
cd /home/isai/Code/SDGKU/issue_mgr

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Heroku deployment"
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "curl https://cli-assets.heroku.com/install.sh | sh"
    exit 1
fi

# Login to Heroku (if not already logged in)
echo "📝 Make sure you're logged in to Heroku..."
heroku auth:whoami || heroku login

# Create Heroku app (you can customize the app name)
echo "🏗️  Creating Heroku app..."
read -p "Enter your Heroku app name (or press Enter for auto-generated): " APP_NAME

if [ -z "$APP_NAME" ]; then
    heroku create
else
    heroku create $APP_NAME
fi

# Set environment variables
echo "🔐 Setting environment variables..."
echo "You'll need to set these manually in Heroku dashboard or via CLI:"
echo "- SECRET_KEY: Generate a new Django secret key"
echo "- DEBUG: Set to False for production"
echo ""
echo "Run these commands:"
echo "heroku config:set SECRET_KEY='your-secret-key-here'"
echo "heroku config:set DEBUG=False"

# Add PostgreSQL addon
echo "🗄️  Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:essential-0

# Deploy to Heroku
echo "📦 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku" || echo "No changes to commit"
git push heroku main || git push heroku master

# Run migrations
echo "🔄 Running database migrations..."
heroku run python manage.py migrate

# Create superuser (optional)
echo "👤 Do you want to create a superuser? (y/n)"
read -r CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ] || [ "$CREATE_SUPERUSER" = "Y" ]; then
    heroku run python manage.py createsuperuser
fi

# Open the app
echo "🎉 Deployment complete! Opening your app..."
heroku open

echo "✅ Your Issue Manager is now live on Heroku!"
echo "📊 Check logs with: heroku logs --tail"
echo "⚙️  Manage your app at: https://dashboard.heroku.com"
