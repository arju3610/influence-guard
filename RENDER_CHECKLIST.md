# Render Deployment Checklist & Troubleshooting

## Quick Fix for "No secrets found" Error

If you're seeing: `Error fetching data: No secrets found. Valid paths for a secrets.toml file...`

**Solution**: The updated `start.py` now creates secrets in multiple locations. After you:
1. Commit and push to GitHub
2. Render will auto-rebuild 
3. Secrets should be found this time ✅

## Pre-Deployment Checklist

### 1. Verify Local Code
- [ ] `app.py` first line is `import pandas as pd` (NOT `nimport...`)
- [ ] Run locally: `python start.py` - should start without errors
- [ ] Test Creator Analysis page locally
- [ ] All pages load without errors

### 2. Commit to Git
```bash
git add .
git commit -m "Fix deployment - secrets and app.py syntax"
git push origin main
```

### 3. Check Render Environment Variables
In your Render dashboard → Your service → **Environment**, verify ALL 7 are set:

```
✓ PYTHONUNBUFFERED = true
✓ YOUTUBE_API_KEY = (actual key from Google Cloud Console)
✓ MYSQL_HOST = (database host/IP)
✓ MYSQL_PORT = 3306 (or your port)
✓ MYSQL_USER = (database username)
✓ MYSQL_PASSWORD = (database password)
✓ MYSQL_DATABASE = (database name)
```

⚠️ **If ANY are missing, app will fail on startup!**

## Deployment Process

1. **Commit code**: `git push origin main`
2. **Render auto-deploys** (watch the logs)
3. **Check Render logs**: Dashboard → Logs tab
4. **Test URL**: https://influence-guard-ai.onrender.com

## Logs to Check

If deployment fails, check Render logs for:
- ✅ "All required environment variables found" = Good!
- ❌ "Missing environment variables" = Set them in Render dashboard
- ❌ "SyntaxError" = Check app.py first line
- ❌ "ModuleNotFoundError" = Package missing from requirements.txt

## Database Connection Issues

If you see "Can't connect to MySQL server":
1. Verify MYSQL_HOST is correct (not localhost - use full IP/hostname)
2. Check database firewall - does it allow Render IPs?
3. Verify database is running and accessible
4. Test locally: `mysql -h MYSQL_HOST -u MYSQL_USER -p`

## Common Errors & Fixes

### Error: "No secrets found"
→ **Fixed in latest update!** Just redeploy after git push

### Error: "ModuleNotFoundError: No module named 'X'"
→ Add to `requirements.txt` and redeploy:
```bash
echo "package-name" >> requirements.txt
git add requirements.txt
git commit -m "Add missing package"
git push origin main
```

### Error: "Invalid syntax" on line 1
→ Check `app.py` first line - should be `import pandas as pd`

### Error: "Can't connect to MySQL server"
→ Check MYSQL_HOST, MYSQL_PORT, firewall, database running status

### App shows login page but Creator Analysis fails
→ YouTube API key invalid or API calls limited
→ Check Google Cloud Console - API enabled? Quota available?

## Verify Deployment Success

Your app is working if:
1. ✅ https://influence-guard-ai.onrender.com loads
2. ✅ You see login page
3. ✅ Can log in with credentials
4. ✅ Creator Analysis page loads
5. ✅ YouTube channel lookup works without "No secrets found" error

## Manual Render Log Inspection

```bash
# SSH into Render (if you have access)
# Or view logs in Render dashboard:
# Dashboard → influence-guard-ai → Logs tab
```

Look for startup messages like:
```
============================================================
INFLUENCE GUARD AI - DEPLOYMENT STARTUP
============================================================

✓ All required environment variables found
✓ Secrets files created:
  - ./.streamlit/secrets.toml
  - /home/container/.streamlit/secrets.toml
✓ Server port: [port]
✓ Working directory: /opt/render/project/src

🚀 Starting Streamlit app...
```

If you see this, deployment succeeded! ✅

## Need Help?

1. Share screenshot of error from app
2. Share Render logs (Logs tab in dashboard)
3. Check: Are ALL 7 environment variables set?
4. Check: Is MYSQL_HOST accessible from Render's servers?
5. Check: Is app.py first line correct?
