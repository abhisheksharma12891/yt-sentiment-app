import streamlit as st
import googleapiclient.discovery
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
st.set_page_config(page_title="YouTube Sentiment Analyzer", page_icon="📊", layout="centered")

# 🔑 SECURE API KEY HANDLING
# This will fetch the key from Streamlit Secrets (Cloud) or local secrets.toml
try:
    API_KEY = st.secrets["YOUTUBE_API_KEY"]
except FileNotFoundError:
    st.error("🚨 API Key not found! Please set it in .streamlit/secrets.toml or Streamlit Cloud Secrets.")
    st.stop()

# --- BACKEND FUNCTIONS ---

def get_sentiment_score(comment_text):
    """
    Analyzes the text using TextBlob and returns a polarity score.
    Score ranges from -1 (Negative) to +1 (Positive).
    """
    analysis = TextBlob(comment_text)
    return analysis.sentiment.polarity

def analyze_video(video_id):
    """
    Fetches comments from YouTube API and analyzes their sentiment.
    """
    try:
        # Initialize Google API Client
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
        
        # Request comments from the video
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50  # Fetching top 50 comments
        )
        response = request.execute()

        data = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            
            # Calculate Sentiment Score
            score = get_sentiment_score(comment)
            
            # Categorize Sentiment
            if score > 0.05:
                mood = "Positive 😊"
            elif score < -0.05:
                mood = "Negative 😡"
            else:
                mood = "Neutral 😐"

            data.append([author, comment, score, mood])

        # Convert to DataFrame for easy handling
        return pd.DataFrame(data, columns=['User', 'Comment', 'Score', 'Mood'])
    
    except Exception as e:
        st.error(f"Error fetching data: {e}. Please check the Video ID.")
        return pd.DataFrame()

# --- FRONTEND UI DESIGN ---

st.title("📊 YouTube Sentiment Analyzer")
st.markdown("### AI-Powered Comment Analysis Tool 🚀")
st.write("Enter a YouTube Video ID to analyze audience sentiment instantly.")

# Input Field
video_id_input = st.text_input("Enter YouTube Video ID:", "yRWdchy43zY", help="You can find the ID in the URL after 'v='")

# Analysis Trigger
if st.button("Analyze Comments ✨"):
    with st.spinner("Fetching and analyzing comments... Please wait..."):
        df = analyze_video(video_id_input)

        if not df.empty:
            # 1. Display Key Metrics
            total = len(df)
            positive = len(df[df['Mood'] == 'Positive 😊'])
            negative = len(df[df['Mood'] == 'Negative 😡'])
            neutral = total - (positive + negative)
            
            # Layout for metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Comments", total)
            col2.metric("Positive", positive, delta="😊")
            col3.metric("Negative", negative, delta="-😡")

            # 2. Visualizations (Bar Chart)
            st.subheader("Sentiment Distribution")
            st.bar_chart(df['Mood'].value_counts())

            # 3. Detailed Data Table
            st.subheader("Comment Insights")
            st.dataframe(df[['User', 'Comment', 'Mood']], use_container_width=True)
        else:
            st.warning("No comments found or Invalid Video ID. Please try again.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ by <b>Abhishek Sharma</b> | Powered by Python & Google API</p>
    </div>
    """, 
    unsafe_allow_html=True
)