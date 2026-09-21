"""AI Chat — a small full-stack web app (FastAPI backend + vanilla JS frontend).

Exposes an OpenAI-compatible ``/api/chat`` endpoint and serves a chat UI at ``/``.
Falls back to a local mock reply when no API key is configured, so the app runs
out of the box for demos and tests.
"""

from __future__ import annotations

import os
from typing import List

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="AI Chat", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


def call_openai(messages: List[ChatMessage]) -> str:
    """Call an OpenAI-compatible chat completion endpoint."""
    payload = {
        "model": MODEL,
        "messages": [m.dict() for m in messages],
        "temperature": 0.3,
    }
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json=payload,
        timeout=60.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def mock_reply(messages: List[ChatMessage]) -> str:
    """Echo the last user message when no API key is configured."""
    last_user = next(
        (m.content for m in reversed(messages) if m.role == "user"), ""
    )
    return f"[mock] You said: {last_user}"


@app.post("/api/chat")
def chat(req: ChatRequest) -> dict:
    """Return an assistant reply for the given conversation."""
    reply = (
        call_openai(req.messages) if OPENAI_API_KEY else mock_reply(req.messages)
    )
    return {"reply": reply}


@app.get("/")
def index():
    """Serve the single-page chat UI."""
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
