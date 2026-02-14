"""
FastAPI Backend for AI-Based Smart Resume Screening System
Handles document upload, embedding generation, and similarity calculation
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from dotenv import load_dotenv

from document_processor import DocumentProcessor
from embedding_generator import EmbeddingGenerator
from similarity_calculator import SimilarityCalculator
from models import RankingResult, RankedResume

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Resume Screening API",
    description="AI-powered resume screening using semantic embeddings",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
doc_processor = DocumentProcessor()
embedding_gen = EmbeddingGenerator()
similarity_calc = SimilarityCalculator()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Resume Screening System API",
        "status": "Online",
        "version": "1.0.0"
    }


@app.post("/screen-resumes", response_model=RankingResult)
async def screen_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    """
    Main endpoint for resume screening

    Args:
        job_description: Job description text
        resumes: List of resume files (PDF/DOCX)

    Returns:
        RankingResult: Ranked resumes with similarity scores
    """
    try:
        # Step 1: Extract text from job description
        jd_text = job_description.strip()
        if not jd_text:
            return JSONResponse(
                status_code=400,
                content={"error": "Job description cannot be empty"}
            )

        # Step 2: Process resumes and extract text
        resume_data = []
        for resume_file in resumes:
            file_content = await resume_file.read()

            # Extract text based on file type
            if resume_file.filename.endswith('.pdf'):
                candidate_name = resume_file.filename.replace('.pdf', '')
                text = doc_processor.extract_from_pdf(file_content)
            elif resume_file.filename.endswith('.docx'):
                candidate_name = resume_file.filename.replace('.docx', '')
                text = doc_processor.extract_from_docx(file_content)
            else:
                continue

            if text:
                resume_data.append({
                    "name": candidate_name,
                    "text": text,
                    "filename": resume_file.filename
                })

        if not resume_data:
            return JSONResponse(
                status_code=400,
                content={"error": "No valid resumes provided"}
            )

        # Step 3: Generate embeddings
        jd_embedding = embedding_gen.generate_embedding(jd_text)

        resume_embeddings = []
        for resume in resume_data:
            embedding = embedding_gen.generate_embedding(resume["text"])
            resume_embeddings.append({
                "name": resume["name"],
                "embedding": embedding,
                "text": resume["text"]
            })

        # Step 4: Calculate similarity scores
        ranked_resumes = []
        for i, resume_emb in enumerate(resume_embeddings):
            similarity_score = similarity_calc.cosine_similarity(
                jd_embedding,
                resume_emb["embedding"]
            )

            ranked_resumes.append(RankedResume(
                rank=i + 1,
                candidate_name=resume_emb["name"],
                similarity_score=round(similarity_score, 4),
                filename=resume_data[i]["filename"]
            ))

        # Step 5: Sort by similarity score (descending)
        ranked_resumes.sort(key=lambda x: x.similarity_score, reverse=True)

        # Update ranks after sorting
        for idx, resume in enumerate(ranked_resumes):
            resume.rank = idx + 1

        return RankingResult(
            total_resumes=len(ranked_resumes),
            ranked_resumes=ranked_resumes,
            status="success"
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing resumes: {str(e)}"}
        )


@app.post("/calculate-similarity")
async def calculate_similarity(
    job_description: str = Form(...),
    resume_text: str = Form(...)
):
    """Calculate similarity between job description and a single resume"""
    try:
        jd_embedding = embedding_gen.generate_embedding(job_description)
        resume_embedding = embedding_gen.generate_embedding(resume_text)

        similarity = similarity_calc.cosine_similarity(jd_embedding, resume_embedding)

        return {
            "similarity_score": round(similarity, 4),
            "status": "success"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/health")
async def health_check():
    """Endpoint to check API health and service availability"""
    return {
        "status": "healthy",
        "services": {
            "api": "online",
            "embedding_service": "online"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
