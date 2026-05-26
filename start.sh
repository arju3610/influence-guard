#!/bin/bash
# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create secrets.toml from environment variables
cat > .streamlit/secrets.toml <<EOF
YOUTUBE_API_KEY = "$YOUTUBE_API_KEY"
MYSQL_HOST = "$MYSQL_HOST"
MYSQL_PORT = $MYSQL_PORT
MYSQL_USER = "$MYSQL_USER"
MYSQL_PASSWORD = "$MYSQL_PASSWORD"
MYSQL_DATABASE = "$MYSQL_DATABASE"
EOF

# Start Streamlit
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
