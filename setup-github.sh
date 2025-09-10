#!/bin/bash

# Interactive Organigram - GitHub Setup Script
# Run this after creating your GitHub repository

echo "🚀 Setting up GitHub repository for Interactive Organigram"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project directory"
    exit 1
fi

echo "📋 Please follow these steps:"
echo ""
echo "1. Go to https://github.com and sign in"
echo "2. Click the '+' icon in the top right"
echo "3. Select 'New repository'"
echo "4. Repository name: 'interactive-organigram'"
echo "5. Description: 'Interactive Organigram with CSV import, editing, and duplicate detection'"
echo "6. Set to PUBLIC (required for free Render.com)"
echo "7. Do NOT initialize with README, .gitignore, or license"
echo "8. Click 'Create repository'"
echo ""

read -p "Have you created the GitHub repository? (y/n): " created_repo

if [ "$created_repo" != "y" ]; then
    echo "Please create the repository first, then run this script again."
    exit 1
fi

echo ""
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ Error: GitHub username is required"
    exit 1
fi

echo ""
echo "🔗 Setting up Git remote..."

# Add the remote repository
git remote add origin https://github.com/$github_username/interactive-organigram.git

# Rename branch to main
git branch -M main

echo ""
echo "📤 Pushing to GitHub..."

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your repository is now on GitHub:"
    echo "🌐 https://github.com/$github_username/interactive-organigram"
    echo ""
    echo "🚀 Next step: Deploy to Render.com"
    echo "1. Go to https://render.com"
    echo "2. Sign up/Sign in"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Connect your GitHub repository"
    echo "5. Use these settings:"
    echo "   - Build Command: npm install"
    echo "   - Start Command: npm start"
    echo "   - Environment: Node"
    echo "6. Click 'Create Web Service'"
    echo ""
    echo "📱 Your app will be live in 2-3 minutes!"
else
    echo "❌ Error: Failed to push to GitHub"
    echo "Please check your GitHub username and repository name"
fi
