"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel
from typing import List, Optional


class RankedResume(BaseModel):
    """Model for a single ranked resume"""
    rank: int
    candidate_name: str
    similarity_score: float
    filename: str


class RankingResult(BaseModel):
    """Model for the complete ranking result"""
    total_resumes: int
    ranked_resumes: List[RankedResume]
    status: str


class SimilarityRequest(BaseModel):
    """Model for similarity calculation request"""
    job_description: str
    resume_text: str


class SimilarityResponse(BaseModel):
    """Model for similarity calculation response"""
    similarity_score: float
    status: str


class HealthCheck(BaseModel):
    """Model for health check response"""
    status: str
    services: dict
