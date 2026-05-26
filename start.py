import os
import sys
from pathlib import Path

# Create .streamlit directory
streamlit_dir = Path(".streamlit")
streamlit_dir.mkdir(exist_ok=True)

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
    print(f"ERROR: Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

# Create secrets.toml
secrets_file = streamlit_dir / "secrets.toml"
with open(secrets_file, "w") as f:
    f.write(f'YOUTUBE_API_KEY = "{env_vars["YOUTUBE_API_KEY"]}"\n')
    f.write(f'MYSQL_HOST = "{env_vars["MYSQL_HOST"]}"\n')
    f.write(f'MYSQL_PORT = {env_vars["MYSQL_PORT"]}\n')
    f.write(f'MYSQL_USER = "{env_vars["MYSQL_USER"]}"\n')
    f.write(f'MYSQL_PASSWORD = "{env_vars["MYSQL_PASSWORD"]}"\n')
    f.write(f'MYSQL_DATABASE = "{env_vars["MYSQL_DATABASE"]}"\n')

print("✓ secrets.toml created successfully")

# Get port from Render
port = os.getenv("PORT", "8501")

# Start Streamlit
os.system(f"streamlit run app.py --server.port={port} --server.address=0.0.0.0")
