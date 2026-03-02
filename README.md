# Stardew Valley Friendship & Gifting Guide Chatbot

**Live URL:** https://stardew-bot-203861284458.us-central1.run.app

## 🌻 What is this chatbot designed to do?
This is a Domain Q&A Chatbot specifically designed to act as an expert guide for **Friendship, Gifting, and Heart Event mechanics** in the video game *Stardew Valley*. 

The chatbot operates within strict boundaries:
* **What it CAN answer:** Loved/hated gifts for specific villagers, how many friendship points certain actions yield, and triggers for villager heart events.
* **What it WILL REFUSE to answer:** Out-of-scope game mechanics such as farming/crop profitability, combat/mines, fishing, real-world questions, or adversarial/harmful prompts. These will trigger a strict refusal response via an LLM escape hatch and a Python regex backstop.

## 🐔 New to Stardew Valley?
*Stardew Valley* is a wildly popular farming simulation role-playing game. While players spend a lot of time growing crops and raising animals, a massive part of the game involves socializing with the locals of "Pelican Town." 

Players can build relationships with over 30 unique villagers by talking to them daily and giving them gifts (up to twice a week). Each villager has their own unique tastes—giving them a "Loved" gift will drastically increase your friendship points, while giving them a "Hated" gift will make them upset and lower your score! As you become better friends, you unlock special cutscenes called "Heart Events." This chatbot helps players navigate these complex social preferences.

---

## 🚀 How to Run Locally

### Prerequisites
* Python 3.10 or higher
* `uv` (Fast Python package installer and resolver)
* A Google Cloud project with Vertex AI enabled.

### 1. Environment Setup
Create a `.env` file in the root directory of this project and add your Google Cloud credentials:
```.env
VERTEX_PROJECT="your-gcp-project-id"
VERTEX_LOCATION="us-central1"
```

### 2. Start the Web Server
Launch the FastAPI server using Uvicorn with this command:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8080
```

Once running, open your web browser and navigate to `http://localhost:8080` to interact with the chatbot!

## 📊 How to Run Evaluations
This project includes an automated evaluation harness that runs 20+ test cases (In-Domain, Out-of-Scope, Adversarial, Golden-Reference MaaJ, and Rubric MaaJ). 

To run the evaluations and print the pass rates by category, run this single command from the root directory:

```bash
uv run python run_evals.py
```