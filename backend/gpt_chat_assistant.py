from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

router = APIRouter()

HUGGINGFACE_API_KEY = os.getenv("")
client = InferenceClient(token=HUGGINGFACE_API_KEY)

# ✅ Use a tested chat-compatible model
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

class Message(BaseModel):
    message: str

@router.post("/ask-assistant")
async def ask_ai(msg: Message):
    try:
        prompt = f"<|user|>{msg.message}\n<|assistant|>"
        response = client.text_generation(
            prompt=prompt,
            model=MODEL_NAME,
            max_new_tokens=200,
            temperature=0.7,
            stop_sequences=["<|user|>"]
        )
        return {"reply": response.strip()}
    except Exception as e:
        return {"reply": f"❌ HuggingFace Error: {str(e)}"}
