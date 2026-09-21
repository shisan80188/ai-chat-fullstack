# AI Chat (Full-Stack)

A small full-stack AI chat application: **FastAPI** backend + **vanilla JS**
frontend, with an OpenAI-compatible chat endpoint.

Runs out of the box in **mock mode** (no API key needed) and switches to a real
model when `OPENAI_API_KEY` is set.

## Stack

- **Backend** — FastAPI, Pydantic, `requests`
- **Frontend** — plain HTML/CSS/JavaScript (no build step)
- **AI** — OpenAI-compatible chat completions API

## Quick start

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# open http://127.0.0.1:8000
```

## Using a real model

```bash
# Any OpenAI-compatible endpoint works
set OPENAI_API_KEY=sk-...        # Windows
set OPENAI_BASE_URL=https://api.openai.com/v1
set OPENAI_MODEL=gpt-4o-mini
uvicorn main:app --reload
```

## API

`POST /api/chat`

```json
{ "messages": [ { "role": "user", "content": "Hello" } ] }
```

Response:

```json
{ "reply": "..." }
```

## Project structure

```
ai-chat-fullstack/
├── main.py          # FastAPI app + /api/chat endpoint
├── index.html       # single-page chat UI
└── requirements.txt
```

## License

MIT
