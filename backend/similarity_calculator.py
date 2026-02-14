"""
Similarity Calculator Module
Calculates cosine similarity between embeddings
"""

import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class SimilarityCalculator:
    """Calculates semantic similarity between embeddings"""

    @staticmethod
    def cosine_similarity(embedding_1: np.ndarray, embedding_2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embedding vectors

        Formula: similarity = (A · B) / (||A|| × ||B||)

        Args:
            embedding_1: First embedding vector
            embedding_2: Second embedding vector

        Returns:
            Cosine similarity score between -1 and 1 (typically 0 to 1 for text)
        """
        try:
            # Calculate dot product
            dot_product = np.dot(embedding_1, embedding_2)

            # Calculate norms
            norm_1 = np.linalg.norm(embedding_1)
            norm_2 = np.linalg.norm(embedding_2)

            # Avoid division by zero
            if norm_1 == 0 or norm_2 == 0:
                logger.warning("One or both embedding vectors have zero norm")
                return 0.0

            # Calculate cosine similarity
            similarity = dot_product / (norm_1 * norm_2)

            # Clamp to [-1, 1] to handle floating point errors
            similarity = np.clip(similarity, -1.0, 1.0)

            return float(similarity)

        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {str(e)}")
            return 0.0

    @staticmethod
    def euclidean_distance(embedding_1: np.ndarray, embedding_2: np.ndarray) -> float:
        """
        Calculate Euclidean distance between two embeddings

        Args:
            embedding_1: First embedding vector
            embedding_2: Second embedding vector

        Returns:
            Euclidean distance (lower = more similar)
        """
        try:
            distance = np.linalg.norm(embedding_1 - embedding_2)
            return float(distance)

        except Exception as e:
            logger.error(f"Error calculating Euclidean distance: {str(e)}")
            return float('inf')

    @staticmethod
    def manhattan_distance(embedding_1: np.ndarray, embedding_2: np.ndarray) -> float:
        """
        Calculate Manhattan distance between two embeddings

        Args:
            embedding_1: First embedding vector
            embedding_2: Second embedding vector

        Returns:
            Manhattan distance (lower = more similar)
        """
        try:
            distance = np.sum(np.abs(embedding_1 - embedding_2))
            return float(distance)

        except Exception as e:
            logger.error(f"Error calculating Manhattan distance: {str(e)}")
            return float('inf')

    @staticmethod
    def batch_similarity(job_embedding: np.ndarray, resume_embeddings: list) -> list:
        """
        Calculate similarity between job embedding and multiple resume embeddings

        Args:
            job_embedding: Job description embedding
            resume_embeddings: List of resume embeddings

        Returns:
            List of similarity scores
        """
        similarities = []
        for resume_embedding in resume_embeddings:
            similarity = SimilarityCalculator.cosine_similarity(
                job_embedding,
                resume_embedding
            )
            similarities.append(similarity)

        return similarities

    @staticmethod
    def rank_by_similarity(similarities: list, resume_names: list) -> list:
        """
        Rank resumes by similarity scores

        Args:
            similarities: List of similarity scores
            resume_names: List of resume names

        Returns:
            Sorted list of (rank, name, score) tuples
        """
        # Create list of (index, score, name)
        indexed_scores = [
            (i, score, name) for i, (score, name) in enumerate(zip(similarities, resume_names))
        ]

        # Sort by score descending
        ranked = sorted(indexed_scores, key=lambda x: x[1], reverse=True)

        # Return with rank numbers
        return [
            (rank + 1, name, score) for rank, (_, score, name) in enumerate(ranked)
        ]

    @staticmethod
    def similarity_percentile(similarity_score: float) -> str:
        """
        Convert similarity score to percentage and relevance label

        Args:
            similarity_score: Score between 0 and 1

        Returns:
            Formatted string with percentage and relevance
        """
        percentage = similarity_score * 100

        if percentage >= 80:
            relevance = "Highly Relevant"
        elif percentage >= 60:
            relevance = "Relevant"
        elif percentage >= 40:
            relevance = "Moderately Relevant"
        else:
            relevance = "Low Relevance"

        return f"{percentage:.2f}% ({relevance})"
