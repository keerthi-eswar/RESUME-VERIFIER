"""
Test suite for Resume Screening System
Run with: pytest tests/
"""

import pytest
import numpy as np
from backend.document_processor import DocumentProcessor
from backend.embedding_generator import EmbeddingGenerator
from backend.similarity_calculator import SimilarityCalculator


class TestDocumentProcessor:
    """Tests for DocumentProcessor"""

    def setup_method(self):
        """Setup test fixtures"""
        self.processor = DocumentProcessor()

    def test_clean_text(self):
        """Test text cleaning functionality"""
        # Test lowercasing
        text = "Hello World"
        cleaned = self.processor.clean_text(text)
        assert "hello" in cleaned
        assert "world" in cleaned

        # Test special character removal
        text = "Test@#$%email.com"
        cleaned = self.processor.clean_text(text)
        assert "@#$%" not in cleaned

    def test_stopwords_removal(self):
        """Test stopword removal"""
        text = "the quick brown fox jumps over the lazy dog"
        cleaned = self.processor.remove_stopwords(text)
        assert "the" not in cleaned.lower()
        assert "quick" in cleaned.lower()
        assert "brown" in cleaned.lower()

    def test_empty_text_handling(self):
        """Test handling of empty text"""
        text = ""
        cleaned = self.processor.clean_text(text)
        assert len(cleaned) == 0

    def test_clean_text_with_numbers(self):
        """Test text cleaning with numbers"""
        text = "5 years of experience with 3+ projects"
        cleaned = self.processor.clean_text(text)
        # Numbers should be removed
        assert "5" not in cleaned
        assert "3" not in cleaned


class TestEmbeddingGenerator:
    """Tests for EmbeddingGenerator"""

    def setup_method(self):
        """Setup test fixtures"""
        self.generator = EmbeddingGenerator()

    def test_embedding_generation(self):
        """Test basic embedding generation"""
        text = "Python development experience"
        embedding = self.generator.generate_embedding(text)

        # Check output type
        assert isinstance(embedding, np.ndarray)

        # Check dimension
        assert len(embedding) > 0

    def test_embedding_dimension(self):
        """Test embedding dimension consistency"""
        dim = self.generator.get_embedding_dimension()
        assert dim == 384  # Default model dimension

    def test_empty_text_embedding(self):
        """Test embedding generation with empty text"""
        embedding = self.generator.generate_embedding("")
        assert len(embedding) == self.generator.get_embedding_dimension()

    def test_batch_embeddings(self):
        """Test batch embedding generation"""
        texts = [
            "Python developer",
            "Java programmer",
            "JavaScript engineer"
        ]
        embeddings = self.generator.generate_batch_embeddings(texts)

        # Check number of embeddings
        assert len(embeddings) == 3

        # Check each embedding dimension
        for emb in embeddings:
            assert len(emb) == 384

    def test_embedding_normalization(self):
        """Test embedding normalization"""
        text = "Test text for normalization"
        embedding = self.generator.generate_embedding(text)
        normalized = self.generator.normalize_embedding(embedding)

        # Check normalized vector has unit length (approximately)
        norm = np.linalg.norm(normalized)
        assert abs(norm - 1.0) < 0.01


class TestSimilarityCalculator:
    """Tests for SimilarityCalculator"""

    def test_cosine_similarity_identical_vectors(self):
        """Test cosine similarity with identical vectors"""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])

        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(1.0, abs=0.01)

    def test_cosine_similarity_orthogonal_vectors(self):
        """Test cosine similarity with orthogonal vectors"""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([0.0, 1.0, 0.0])

        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(0.0, abs=0.01)

    def test_cosine_similarity_opposite_vectors(self):
        """Test cosine similarity with opposite vectors"""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([-1.0, 0.0, 0.0])

        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(-1.0, abs=0.01)

    def test_cosine_similarity_result_range(self):
        """Test that cosine similarity is always between -1 and 1"""
        np.random.seed(42)
        for _ in range(10):
            vec1 = np.random.randn(10)
            vec2 = np.random.randn(10)

            similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
            assert -1 <= similarity <= 1

    def test_euclidean_distance(self):
        """Test Euclidean distance calculation"""
        vec1 = np.array([0.0, 0.0, 0.0])
        vec2 = np.array([3.0, 4.0, 0.0])

        distance = SimilarityCalculator.euclidean_distance(vec1, vec2)
        assert distance == pytest.approx(5.0, abs=0.01)

    def test_batch_similarity(self):
        """Test batch similarity calculation"""
        job_vec = np.array([0.5, 0.3, 0.8])
        resume_vecs = [
            np.array([0.5, 0.3, 0.8]),
            np.array([0.4, 0.2, 0.7]),
            np.array([0.1, 0.1, 0.1])
        ]

        similarities = SimilarityCalculator.batch_similarity(job_vec, resume_vecs)

        assert len(similarities) == 3
        assert all(isinstance(s, float) for s in similarities)
        assert similarities[0] > similarities[2]  # First more similar than last

    def test_zero_vector_handling(self):
        """Test handling of zero vectors"""
        vec1 = np.array([0.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])

        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity == 0.0


class TestIntegration:
    """Integration tests for the full pipeline"""

    def setup_method(self):
        """Setup test fixtures"""
        self.processor = DocumentProcessor()
        self.generator = EmbeddingGenerator()
        self.calculator = SimilarityCalculator()

    def test_full_pipeline(self):
        """Test complete pipeline from text to similarity score"""
        job_desc = "Senior Python developer with FastAPI experience and PostgreSQL knowledge"
        resume_text = "Python expert with 5 years FastAPI development and database management"

        # Process texts
        job_cleaned = self.processor.clean_text(job_desc)
        resume_cleaned = self.processor.clean_text(resume_text)

        # Generate embeddings
        job_emb = self.generator.generate_embedding(job_cleaned)
        resume_emb = self.generator.generate_embedding(resume_cleaned)

        # Calculate similarity
        similarity = self.calculator.cosine_similarity(job_emb, resume_emb)

        # Should have high similarity
        assert 0 <= similarity <= 1
        assert similarity > 0.5  # Should be reasonably similar

    def test_different_keywords_same_meaning(self):
        """Test that different keywords with same meaning get high similarity"""
        job_desc = "REST API development"
        resume_text = "Web service API building"

        job_emb = self.generator.generate_embedding(job_desc)
        resume_emb = self.generator.generate_embedding(resume_text)

        similarity = self.calculator.cosine_similarity(job_emb, resume_emb)

        # Should have moderate to high similarity despite different keywords
        assert similarity > 0.4


# Performance Tests
class TestPerformance:
    """Performance and scalability tests"""

    def test_embedding_speed(self):
        """Test embedding generation speed"""
        import time

        generator = EmbeddingGenerator()
        text = "Senior Python Developer with extensive experience"

        start = time.time()
        embedding = generator.generate_embedding(text)
        elapsed = time.time() - start

        # Should complete within reasonable time
        assert elapsed < 1.0  # Less than 1 second

    def test_batch_processing_efficiency(self):
        """Test batch processing efficiency"""
        import time

        generator = EmbeddingGenerator()
        texts = ["Text " + str(i) for i in range(10)]

        start = time.time()
        embeddings = generator.generate_batch_embeddings(texts)
        elapsed = time.time() - start

        assert len(embeddings) == 10
        assert elapsed < 5.0  # Should be reasonably fast


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
