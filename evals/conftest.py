import json
import sys
from pathlib import Path
from litellm import completion

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import MODEL, build_messages, apply_backstop

JUDGE_MODEL = "vertex_ai/gemini-2.5-flash"

def get_review(text: str) -> str:
    messages = build_messages(text)
    response = completion(model=MODEL, messages=messages)
    raw_text = response.choices[0].message.content
    return apply_backstop(text, raw_text)

JUDGE_SYSTEM_GOLDEN = """You are an expert evaluator. Given a prompt, a reference response, and a generated response, rate the overall quality of the generated response on a scale of 1 to 10 based on how well it matches the facts of the reference. Output JSON: {"rating": <int>}"""

JUDGE_SYSTEM_RUBRIC = """You are an expert evaluator. Given a prompt, a generated response, and a rubric, rate the quality of the response from 1 to 10 based on how well it satisfies the rubric. Output JSON: {"rating": <int>}"""

def judge_with_golden(prompt: str, reference: str, response: str) -> int:
    user_msg = f"<prompt>\n{prompt}\n</prompt>\n<reference>\n{reference}\n</reference>\n<response>\n{response}\n</response>"
    res = completion(model=JUDGE_MODEL, messages=[{"role": "system", "content": JUDGE_SYSTEM_GOLDEN}, {"role": "user", "content": user_msg}], response_format={"type": "json_object"})
    return json.loads(res.choices[0].message.content)["rating"]

def judge_with_rubric(prompt: str, response: str, rubric: str) -> int:
    user_msg = f"<prompt>\n{prompt}\n</prompt>\n<response>\n{response}\n</response>\n<rubric>\n{rubric}\n</rubric>"
    res = completion(model=JUDGE_MODEL, messages=[{"role": "system", "content": JUDGE_SYSTEM_RUBRIC}, {"role": "user", "content": user_msg}], response_format={"type": "json_object"})
    return json.loads(res.choices[0].message.content)["rating"]