import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def fetch_all_serp_data(query, country="us"):
    try:
        # 📰 News Search
        news_url = f"https://serpapi.com/search.json?q={query}&tbm=nws&location={country}&api_key={SERP_API_KEY}"
        news_res = requests.get(news_url).json()
        news = news_res.get("news_results", [])

        # 🖼️ Image Search
        image_url = f"https://serpapi.com/search.json?q={query}&tbm=isch&location={country}&api_key={SERP_API_KEY}"
        img_res = requests.get(image_url).json()
        images = img_res.get("images_results", [])

        return {"news": news, "images": images}
    except Exception as e:
        return {"error": str(e), "news": [], "images": []}
