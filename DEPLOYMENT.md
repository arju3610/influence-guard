# Render Deployment Guide for Influence Guard AI

## Prerequisites
1. A GitHub account with your project pushed to a repository
2. A Render account (https://render.com)
3. Your secrets configured in Render environment variables

## Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Step 2: Create Render Account and Connect GitHub
1. Go to https://render.com and sign up
2. Click "New +" button and select "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account
5. Select your repository

## Step 3: Configure the Web Service
1. **Name**: `influence-guard-ai` (or your preferred name)
2. **Runtime**: Python 3.11
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. **Plan**: Free tier (or paid if needed)

## Step 4: Add Environment Variables
In the Render dashboard, add these environment variables:

```
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
MYSQL_HOST=YOUR_DATABASE_HOST
MYSQL_PORT=YOUR_DATABASE_PORT
MYSQL_USER=YOUR_DATABASE_USER
MYSQL_PASSWORD=YOUR_DATABASE_PASSWORD
MYSQL_DATABASE=YOUR_DATABASE_NAME
PYTHONUNBUFFERED=true
```

**Important**: Do NOT commit these values to git. Only add them in Render's environment variables dashboard.

## Step 5: Create Streamlit Secrets
For local development, create `.streamlit/secrets.toml`:
```toml
YOUTUBE_API_KEY = "YOUR_API_KEY"
MYSQL_HOST = "YOUR_HOST"
MYSQL_PORT = YOUR_PORT
MYSQL_USER = "YOUR_USER"
MYSQL_PASSWORD = "YOUR_PASSWORD"
MYSQL_DATABASE = "YOUR_DATABASE"
```

**Note**: This file is in `.gitignore` so it won't be committed.

## Step 6: Deploy
1. Click "Create Web Service" in Render
2. Render will automatically build and deploy
3. Access your app at `https://YOUR_SERVICE_NAME.onrender.com`

## Troubleshooting

### App crashes on startup
- Check logs in Render dashboard
- Ensure all dependencies in `requirements.txt` are listed
- Verify environment variables are set correctly

### Port issues
- Render assigns a random port via `$PORT` environment variable
- The start command already handles this: `--server.port=$PORT`

### Database connection fails
- Verify database credentials in environment variables
- Check if database is accessible from Render's servers
- Consider using a managed database service (Railway, Supabase, etc.)

### Missing modules
- Update `requirements.txt` with missing packages
- Commit changes to git
- Render will auto-rebuild on push

## Important Notes
- Keep `requirements.txt` updated with all dependencies
- The free tier has limitations (15-minute auto-spin-down)
- Consider upgrading to a paid plan for production use
- Always use environment variables for sensitive data
