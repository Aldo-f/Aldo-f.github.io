#!/usr/bin/env python3
"""FastAPI wrapper around the OKF RAG pipeline.

POST /search with {"question": "...", "k": 3} returns {answer, sources, confidence}.
Run: uvicorn rag_api:app --host 0.0.0.0 --port 8000
(or ./scripts/run_rag_api.sh from the bundle root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "rag"))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag_query import OKFRAGPipeline

app = FastAPI(title="OKF RAG API")
pipeline = OKFRAGPipeline(bundle_path=str(Path(__file__).resolve().parent.parent))


class QueryPayload(BaseModel):
    question: str
    k: int = 3


@app.post("/search")
async def search(payload: QueryPayload):
    try:
        return pipeline.query_with_answer(payload.question, k=payload.k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
