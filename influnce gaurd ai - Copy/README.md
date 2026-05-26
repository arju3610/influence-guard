# Influence Guard AI

An AI-powered platform for detecting fake YouTube influencers using advanced analytics and machine learning.

## Features

- **Real-time YouTube Data Fetching**: Integrates with YouTube API to fetch channel statistics
- **Fraud Detection AI**: Uses rule-based and ML-powered algorithms to detect fake accounts
- **Interactive Dashboards**: Visualize influencer data with modern UI
- **History Tracking**: Store and analyze past analyses in MySQL database
- **AI Insights**: Get detailed recommendations based on analysis

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd influence-guard-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up secrets**
   - Create `.streamlit/secrets.toml`
   - Add your YouTube API key and MySQL credentials:
     ```
     YOUTUBE_API_KEY = "your-api-key"
     MYSQL_HOST = "localhost"
     MYSQL_USER = "your-user"
     MYSQL_PASSWORD = "your-password"
     MYSQL_DATABASE = "influence_guard_ai"
     ```

4. **Set up MySQL database**
   - Create database `influence_guard_ai`
   - Run the following SQL to create table:
     ```sql
     CREATE TABLE influencer_history (
         id INT AUTO_INCREMENT PRIMARY KEY,
         channel_name VARCHAR(255),
         subscribers INT,
         views INT,
         videos INT,
         engagement FLOAT,
         fraud_score INT,
         status VARCHAR(50),
         analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Navigate to "YouTube Analytics" page
2. Enter a YouTube Channel ID
3. Click "Analyze Channel" to get instant results
4. View dashboards and insights across different pages

## Project Structure

- `app.py`: Main Streamlit application
- `pages/`: Individual dashboard pages
- `youtube_api.py`: YouTube API integration
- `model.py`: AI model for fraud detection
- `database.py`: Database operations
- `insights.py`: AI insights generation
- `styles.py`: UI styling

## Technologies Used

- Streamlit for web app
- YouTube Data API v3
- Scikit-learn for ML
- Plotly for visualizations
- MySQL for data storage
- Pandas for data processing

## Future Enhancements

- Integrate more social media platforms
- Advanced ML models with training data
- Real-time monitoring
- API endpoints for external integrations