# demand_api_backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pytrends_fetcher import auto_trend_analysis_by_search
from serp_api_scraper import fetch_all_serp_data
from gpt_chat_assistant import router as assistant_router

app = FastAPI(title="AI Demand Analyzer Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include GPT assistant router
app.include_router(assistant_router)

@app.get("/")
def read_root():
    return {"message": "✅ AI Demand Analyzer Backend is Running!"}

@app.get("/analyze-demand")
def analyze_demand(product: str):
    try:
        trends = auto_trend_analysis_by_search(product)
        serp_data = fetch_all_serp_data(product, "US")

        return {
            "status": "success",
            "product": product,
            "trends": trends,
            "news": serp_data.get("news", []),
            "images": serp_data.get("images", [])
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
