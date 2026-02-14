"""
Embedding Generator Module
Generates semantic embeddings using Azure OpenAI or open-source models
"""

import os
from typing import List
import numpy as np
import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates semantic embeddings for text using SentenceTransformer"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding generator

        Args:
            model_name: SentenceTransformer model to use
                       - "all-MiniLM-L6-v2" (lightweight, 384 dimensions)
                       - "all-mpnet-base-v2" (better quality, 768 dimensions)
                       - For production: Use Azure OpenAI text-embedding-ada-002
        """
        self.model_name = model_name
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            # Fallback to lightweight model
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding vector for input text

        Args:
            text: Input text to embed

        Returns:
            Embedding vector as numpy array
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return np.zeros(self.get_embedding_dimension())

            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)

            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return np.zeros(self.get_embedding_dimension())

    def generate_batch_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts efficiently

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return list(embeddings)

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            return [np.zeros(self.get_embedding_dimension()) for _ in texts]

    def get_embedding_dimension(self) -> int:
        """
        Get dimension of embedding vectors

        Returns:
            Embedding dimension
        """
        # Create a dummy embedding to determine dimension
        dummy_embedding = self.model.encode("test")
        return len(dummy_embedding)

    def normalize_embedding(self, embedding: np.ndarray) -> np.ndarray:
        """
        Normalize embedding vector to unit length

        Args:
            embedding: Input embedding vector

        Returns:
            Normalized embedding
        """
        norm = np.linalg.norm(embedding)
        if norm > 0:
            return embedding / norm
        return embedding


# Note: For production deployment with Azure OpenAI integration, use this class instead:
"""
class AzureOpenAIEmbedding:
    def __init__(self, api_key: str, endpoint: str, model_name: str = "text-embedding-ada-002"):
        from openai import AzureOpenAI
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint
        )
        self.model_name = model_name
        self.embedding_dimension = 1536  # Ada model dimension

    def generate_embedding(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            input=text,
            model=self.model_name
        )
        return np.array(response.data[0].embedding)
"""
