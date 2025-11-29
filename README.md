# 📊 YouTube Sentiment Analyzer (AI-Powered)

An automated tool that extracts comments from any YouTube video and performs real-time sentiment analysis to understand audience reaction.

🔗 **Live Demo:** [Click Here to View App](https://yt-sentiment-app.streamlit.app/ ) 

## 🧐 What It Does
1. **Extraction:** Uses **YouTube Data API v3** to fetch comments from a video ID.
2. **Analysis:** Uses **TextBlob (NLP)** to classify comments into Positive, Negative, or Neutral.
3. **Visualization:** Displays interactive charts and metrics using **Streamlit**.

## 🛠️ Tech Stack
- **Python 3.11**
- **Streamlit** (Frontend)
- **Google API Client** (Data Extraction)
- **TextBlob** (Natural Language Processing)
- **Pandas** (Data Management)

## 🚀 How to Run Locally

1. **Clone the repo**
   ```bash
   git clone [https://github.com/abhisheksharma12891/yt-sentiment-app.git](https://github.com/abhisheksharma12891/yt-sentiment-app.git)

## Install Dependencies
   pip install -r requirements.txt

## Add API Key
  Get your API Key from Google Cloud Console.
  Update the API_KEY variable in app.py.

## Run the App
  streamlit run app.py
