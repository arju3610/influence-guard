import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest


# ---------------- LOAD DATA ----------------
def load_data(file):
    try:
        df = pd.read_csv(file)

        if 'account_id' in df.columns:
            df['account_id'] = df['account_id'].astype(str).str.lower()

        return df

    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()


# ---------------- PROCESS DATA ----------------
def process_data(df):

    if df.empty:
        return df

    df = df.copy()

    try:
        # ---------------- SAFE DEFAULTS ----------------
        required_cols = ['likes', 'comments', 'shares', 'saves', 'followers_gained', 'follower_count']

        for col in required_cols:
            if col not in df.columns:
                df[col] = 0

        df['follower_count'] = df['follower_count'].replace(0, 1)

        # ---------------- FEATURES ----------------
        df['total_engagement'] = (
            df['likes'] + df['comments'] + df['shares'] + df['saves']
        )

        df['engagement_ratio'] = df['total_engagement'] / df['follower_count']
        df['growth_rate'] = df['followers_gained'] / df['follower_count']

        # ---------------- ML MODEL ----------------
        model = IsolationForest(contamination=0.27, random_state=42)

        df['anomaly'] = model.fit_predict(
            df[['follower_count', 'likes', 'comments', 'shares', 'saves', 'engagement_ratio']]
        )

        # ---------------- RULES ----------------
        df['low_engagement_flag'] = df['engagement_ratio'] < 0.01
        df['high_growth_flag'] = df['growth_rate'] > 0.5

        df['final_flag'] = (
            (df['anomaly'] == -1) |
            (df['low_engagement_flag']) |
            (df['high_growth_flag'])
        )

        # ---------------- FAKE FOLLOWERS ----------------
        df['fake_followers'] = (
            df['follower_count'] * (
                0.6 * (df['engagement_ratio'] < 0.01).astype(int) +
                0.3 * (df['growth_rate'] > 0.5).astype(int) +
                0.1 * (df['engagement_ratio'] < 0.02).astype(int)
            )
        ).astype(int)

        # ---------------- FAKE RATIO ----------------
        df['fake_followers_ratio'] = df['fake_followers'] / df['follower_count']

        # ---------------- INFLUENCE SCORE (IMPROVED) ----------------
        df['influence_score'] = (
            (df['engagement_ratio'] * 50) +
            (df['growth_rate'] * 30) +
            (df['follower_count'] / df['follower_count'].max() * 20)
        ).round(2)

        # ---------------- FINAL STATUS (REAL / SUSPICIOUS / FAKE) ----------------
        def classify_account(row):
            # Fake: Has both anomaly flags AND high fake follower ratio
            if row['final_flag'] and row['fake_followers_ratio'] > 0.15:
                return "Fake"
            # Suspicious: Has either anomaly flags OR high fake follower ratio
            elif row['final_flag'] or row['fake_followers_ratio'] > 0.15:
                return "Suspicious"
            # Real: Everything else
            else:
                return "Real"

        df['account_status'] = df.apply(classify_account, axis=1)

        # ---------------- SAVE MODEL ----------------
        joblib.dump(model, "model.pkl")

    except Exception as e:
        print(f"Processing Error: {e}")

    return df


# ---------------- ACCOUNT ANALYSIS ----------------
def get_account_analysis(df, account_id):

    if df.empty:
        return None

    user = df[df['account_id'] == account_id]

    if user.empty:
        return None

    user = user.iloc[0]

    return {
        "followers": int(user['follower_count']),
        "total_engagement": int(user['total_engagement']),
        "engagement_ratio": float(user['engagement_ratio']),
        "growth_rate": float(user['growth_rate']),
        "influence_score": float(user['influence_score']),
        "fake_followers": int(user['fake_followers']),
        "status": user['account_status']
    }