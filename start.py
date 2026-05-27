import os
import sys
from pathlib import Path

print("=" * 60)
print("INFLUENCE GUARD AI - DEPLOYMENT STARTUP")
print("=" * 60)

# Read environment variables
env_vars = {
    "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY", ""),
    "MYSQL_HOST": os.getenv("MYSQL_HOST", ""),
    "MYSQL_PORT": os.getenv("MYSQL_PORT", ""),
    "MYSQL_USER": os.getenv("MYSQL_USER", ""),
    "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD", ""),
    "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE", ""),
}

# Check if all required variables are set
required_vars = ["YOUTUBE_API_KEY", "MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]
missing = [var for var in required_vars if not env_vars[var]]

if missing:
    print("\n❌ ERROR: Missing environment variables!")
    print(f"\nPlease set these variables in Render dashboard:")
    for var in missing:
        print(f"  - {var}")
    print("\nDeployment guide: https://render.com/docs/environment-variables")
    print("=" * 60)
    sys.exit(1)

print("\n✓ All required environment variables found")
print(f"  - YOUTUBE_API_KEY: {env_vars['YOUTUBE_API_KEY'][:10]}***")
print(f"  - MYSQL_HOST: {env_vars['MYSQL_HOST']}")
print(f"  - MYSQL_DATABASE: {env_vars['MYSQL_DATABASE']}")

# Create .streamlit directory in both local and home locations
streamlit_dir_local = Path(".streamlit")
streamlit_dir_local.mkdir(exist_ok=True)

# Also create in home directory for Render
home = Path.home()
streamlit_dir_home = home / ".streamlit"
streamlit_dir_home.mkdir(exist_ok=True, parents=True)

# Write secrets to both locations
secrets_content = f'''YOUTUBE_API_KEY = "{env_vars["YOUTUBE_API_KEY"]}"
MYSQL_HOST = "{env_vars["MYSQL_HOST"]}"
MYSQL_PORT = {env_vars["MYSQL_PORT"]}
MYSQL_USER = "{env_vars["MYSQL_USER"]}"
MYSQL_PASSWORD = "{env_vars["MYSQL_PASSWORD"]}"
MYSQL_DATABASE = "{env_vars["MYSQL_DATABASE"]}"
'''

created_files = []

# Write to local .streamlit/secrets.toml
try:
    secrets_file_local = streamlit_dir_local / "secrets.toml"
    with open(secrets_file_local, "w") as f:
        f.write(secrets_content)
    created_files.append(str(secrets_file_local))
except Exception as e:
    print(f"⚠️  Warning: Could not create local secrets file: {e}")

# Write to home .streamlit/secrets.toml
try:
    secrets_file_home = streamlit_dir_home / "secrets.toml"
    with open(secrets_file_home, "w") as f:
        f.write(secrets_content)
    created_files.append(str(secrets_file_home))
except Exception as e:
    print(f"⚠️  Warning: Could not create home secrets file: {e}")

if created_files:
    print(f"✓ Secrets files created:")
    for f in created_files:
        print(f"  - {f}")
else:
    print("❌ Could not create any secrets files!")
    sys.exit(1)

# Get port from Render
port = os.getenv("PORT", "8501")
print(f"✓ Server port: {port}")
print(f"✓ Working directory: {os.getcwd()}")
print(f"✓ Home directory: {home}")
print("=" * 60)
print("\n🚀 Starting Streamlit app...\n")

# Start Streamlit
exit_code = os.system(f"streamlit run app.py --server.port={port} --server.address=0.0.0.0")
sys.exit(exit_code)
