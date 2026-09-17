# AthleteOS

Async FastAPI skeleton with LangChain, LangGraph, and Pydantic.

## Stack

Python 3.13 · FastAPI (async routes) · LangChain · LangGraph · OpenAI / Gemini (REST) / Anthropic (`LLM_PROVIDER`)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Set the API key for your provider in `.env`. See `.env.example` for variables.

## Run

```bash
python -m app.main
```

Docs: http://127.0.0.1:8000/docs

| Method | Path | Body |
|--------|------|------|
| GET | `/health` | — |
| POST | `/agent/run` | `{"message": "..."}` |

## Docker

```bash
docker build -t athlete-os .
docker run --rm -p 8000:8000 --env-file .env athlete-os
```

## Notebook

Start the API first, then:

```bash
jupyter notebook notebooks/test.ipynb
```
