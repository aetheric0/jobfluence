#!/usr/bin/env python3
'''
JobFluence Demo Version API route
'''

from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.parser import parse_document
from datetime import datetime

router = APIRouter(prefix='/demo', tags=['demo'])
templates = Jinja2Templates(directory='templates')

# Load the pre-trained Sentence Transformer model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def compute_semantic_match(resume_text: str, job_description: str) -> float:
    """
    Computes semantic similarity between the resume and job description
    using sentence embeddings and cosine similarity.
    """
    # Generate embeddings for both texts
    resume_embedding = embedder.encode(resume_text)
    job_embedding = embedder.encode(job_description)

    # Compute cosine similarity
    similarity_score = cosine_similarity(
        [resume_embedding], [job_embedding]
    )[0][0]

    # Convert similarity to percentage for easier interpretation
    return round(similarity_score * 100, 2)

@router.get("/", response_class=HTMLResponse)
async def demo_form(request: Request):
    return templates.TemplateResponse("demo.html", {
        "request": request,
        "match_percentage": None,     # Initialize with default values
        "resume_text": "",
        "job_description": "",
        "now": datetime.now,
    })

@router.post("/match", response_class=HTMLResponse)
async def demo_match(
    request: Request,
    job_description: str = Form(...),
    file: UploadFile = File(...)
):
    file_bytes = await file.read()
    try:
        resume_text = parse_document(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Compute similarity
    match_percentage = compute_semantic_match(resume_text, job_description)

    return templates.TemplateResponse(
        "demo.html",
        {
            "request": request,
            "resume_text": resume_text,
            "job_description": job_description,
            "match_percentage": match_percentage,
            "now": datetime.now,
        },
    )
