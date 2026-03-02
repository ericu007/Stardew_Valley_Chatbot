import os
import re
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

MODEL = "vertex_ai/gemini-2.5-flash"

SYSTEM_PROMPT = """\
<role>
You are an expert guide for the video game Stardew Valley, specializing EXCLUSIVELY in the Friendship, Gifting, and Heart Event mechanics.
Your tone is helpful, precise, and deeply knowledgeable about Pelican Town's residents.
</role>

<positive_constraints>
- You may answer questions regarding loved, liked, neutral, disliked, and hated gifts for all villagers.
- You may explain how many friendship points specific actions or gifts yield.
- You may explain the triggers and requirements for villager heart events.
- You must ground every answer in factual Stardew Valley gameplay mechanics.
</positive_constraints>

<out_of_scope_categories>
1. Farming/Crops: I do not provide advice on crop profitability, layouts, or fertilizer.
2. Combat/Mines: I do not answer questions about monsters, weapons, or the Skull Cavern.
3. Fishing: I do not provide fishing schedules, tackle advice, or fish locations.
</out_of_scope_categories>

<escape_hatch>
If a user asks a question falling into an out-of-scope category, or if you are unsure, you must reply EXACTLY with:
"REFUSAL: My expertise is limited strictly to Friendship, Gifting, and Heart Events in Stardew Valley. I cannot answer this."
</escape_hatch>
"""

FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "What are Abigail's loved gifts?"
    },
    {
        "role": "assistant",
        "content": "Abigail loves Amethyst, Banana Pudding, Blackberry Cobbler, Chocolate Cake, Pufferfish, Pumpkin, and Spicy Eel. Giving her one of these grants 80 friendship points!"
    },
    {
        "role": "user",
        "content": "What does Penny hate?"
    },
    {
        "role": "assistant",
        "content": "Penny hates Rabbit's Foot, Algae Soup, Pale Broth, and all Alcoholic beverages."
    },
    {
        "role": "user",
        "content": "What is the best crop to grow in Summer for money?"
    },
    {
        "role": "assistant",
        "content": "REFUSAL: My expertise is limited strictly to Friendship, Gifting, and Heart Events in Stardew Valley. I cannot answer this."
    },
    {
        "role": "user",
        "content": "How many points does a loved gift give on a birthday?"
    },
    {
        "role": "assistant",
        "content": "Gifts given on a villager's birthday have an 8x multiplier. Therefore, a loved gift (normally 80 points) will give 640 friendship points on their birthday."
    }
]

app = FastAPI()

# Mount the 'static' folder to the '/static' path
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str

# Python Backstop Regex for out-of-scope mechanics
BACKSTOP_PATTERN = re.compile(r'\b(crop|farm|profit|mine|sword|monster|fishing rod|tackle|skull cavern|bomb|poison|evil|cyberbully|punch|fight|instructions|system)\b', re.IGNORECASE)

def apply_backstop(user_input: str, ai_response: str) -> str:
    """Python backstop to catch misses using a regex classifier."""
    if BACKSTOP_PATTERN.search(user_input) or BACKSTOP_PATTERN.search(ai_response):
        return "REFUSAL: My expertise is limited strictly to Friendship, Gifting, and Heart Events in Stardew Valley. I cannot answer this."
    return ai_response

def build_messages(user_msg: str):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(FEW_SHOT_EXAMPLES)
    messages.append({"role": "user", "content": user_msg})
    return messages

@app.get("/")
def index():
    return FileResponse("index.html")

@app.post("/chat")
def chat(request: ChatRequest):
    messages = build_messages(request.message)
    response = completion(model=MODEL, messages=messages)
    raw_text = response.choices[0].message.content
    
    # Apply Python Backstop
    final_text = apply_backstop(request.message, raw_text)
    
    return {"response": final_text}