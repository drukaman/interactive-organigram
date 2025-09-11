# 🚀 GitHub & Render.com Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it: `interactive-organigram`
5. Add description: `Interactive Organigram with CSV import, editing, and duplicate detection`
6. Set to **Public** (required for free Render.com deployment)
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, run these commands in your terminal:

```bash
# Navigate to your project directory
cd /Users/andreferreira/Desktop/Dev/techtree/nodes_organigram

# Add the remote repository (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/interactive-organigram.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Render.com

1. Go to [Render.com](https://render.com) and sign up/sign in
2. Click "New +" and select "Web Service"
3. Connect your GitHub account if not already connected
4. Select your `interactive-organigram` repository
5. Configure the deployment:
   - **Name**: `interactive-organigram`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Instance Type**: `Free` (for testing)
6. Click "Create Web Service"

## Step 4: Environment Configuration

Render.com will automatically:

- Set the `PORT` environment variable
- Install dependencies with `npm install`
- Start the server with `npm start`

## Step 5: Access Your Application

After deployment (2-3 minutes), you'll get a URL like:
`https://interactive-organigram-XXXX.onrender.com`

## 🔧 Deployment Features

Your application includes:

- ✅ **Express.js server** for production hosting
- ✅ **Health check endpoint** at `/health`
- ✅ **Static file serving** for all assets
- ✅ **Environment variable support**
- ✅ **Automatic HTTPS** via Render.com

## 📁 Deployed Files

The following files will be deployed:

- `index.html` - Main application
- `server.js` - Express.js server
- `package.json` - Node.js dependencies
- `nodes_hierarchy.json` - Sample data
- All Python tools (for reference)

## 🛠️ Post-Deployment

After deployment:

1. Test the application functionality
2. Try importing CSV files
3. Test the editing features
4. Verify duplicate detection works
5. Update the README with your live URL

## 🔄 Updates

To update your deployed application:

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push origin main
```

Render.com will automatically redeploy when you push to the main branch.

---

**Your application will be live and accessible to anyone with the URL!**
