# AI-Based Smart Resume Screening System

## 📋 Project Overview

An intelligent, cloud-ready resume screening system that ranks resumes based on semantic similarity with job descriptions using Machine Learning embeddings. Unlike traditional keyword-based ATS systems, this system understands contextual meaning and captures semantic relationships between job requirements and candidate qualifications.

### Key Features
- 🤖 **Semantic Understanding**: Uses embeddings to understand meaning beyond keywords
- 📊 **Smart Ranking**: Ranks resumes by relevance using cosine similarity
- ⚡ **Fast Processing**: Batch processing of multiple resumes
- 🎯 **Scalable**: Cloud-ready REST API architecture
- 📱 **User-Friendly**: Web interface for recruiters
- 📥 **Multiple Formats**: Supports PDF and DOCX resumes

---

## 🏗️ Project Structure

```
resume-screening-system/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── document_processor.py    # PDF/DOCX text extraction
│   ├── embedding_generator.py   # Semantic embeddings
│   ├── similarity_calculator.py # Cosine similarity calculation
│   └── models.py               # Pydantic data models
├── frontend/
│   └── app.py                  # Streamlit web interface
├── utils/
│   ├── __init__.py
│   ├── file_handler.py         # File utilities
│   └── logger.py               # Logging configuration
├── sample_data/
│   ├── sample_job_description.txt
│   └── sample_resume.txt
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── README.md                   # This file
├── SETUP_GUIDE.md              # Detailed setup instructions
└── DEPLOYMENT.md               # Deployment guide
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Optional: Azure account (for production deployment)

### Installation

1. **Clone/Download the project**
```bash
cd resume-screening-system
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your settings (optional for basic usage)
```

5. **Run the backend API**
```bash
python -m backend.main
```
The API will start at `http://localhost:8000`

6. **In a new terminal, run the frontend**
```bash
streamlit run frontend/app.py
```
The interface will open at `http://localhost:8501`

---

## 📖 How to Use

### Step 1: Prepare Job Description
- Copy your job description text
- Paste it in the "Job Description" field in the web interface

### Step 2: Upload Resumes
- Click "Upload Resumes" button
- Select one or multiple PDF or DOCX files
- Supported formats: `.pdf`, `.docx`

### Step 3: Run Analysis
- Click "🔍 Screen Resumes" button
- Wait for processing to complete

### Step 4: View Results
- See ranked candidates with similarity scores
- Download results as CSV
- View detailed analysis metrics

---

## 🔧 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Python**: Core language
- **Sentence Transformers**: Pre-trained embedding models
- **Scikit-learn**: Machine learning utilities
- **PyPDF2**: PDF parsing
- **python-docx**: DOCX parsing

### Frontend
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **Requests**: HTTP client

### ML/NLP
- **Transformers (BERT)**: Pre-trained language models
- **NumPy**: Numerical computing
- **Cosine Similarity**: Ranking algorithm

---

## 📊 Algorithm Explanation

### Cosine Similarity Formula
```
Similarity = (A · B) / (||A|| × ||B||)

Where:
- A = Job description embedding vector
- B = Resume embedding vector
- · = Dot product
- ||X|| = Vector norm (magnitude)
```

### Process Flow
1. **Text Extraction**: Convert PDF/DOCX → Plain text
2. **Preprocessing**: Remove special characters, normalize text
3. **Embedding Generation**: Convert text → semantic vectors (1536 dimensions)
4. **Similarity Calculation**: Compute cosine similarity between JD and resumes
5. **Ranking**: Sort resumes by scores (descending)
6. **Display**: Show ranked results with metrics

---

## 📝 Sample Usage

### Input Example
**Job Description:**
```
We're looking for a Python Developer with 3+ years experience.
Must have knowledge of FastAPI, PostgreSQL, and AWS.
Experience with Docker and Kubernetes is preferred.
```

**Resume:**
```
John Doe - Senior Python Developer
- 5 years of Python development experience
- Expertise in FastAPI and Django
- PostgreSQL and MySQL database management
- AWS and Docker containerization
- Kubernetes orchestration
```

### Output Example
```
Rank  Candidate Name     Similarity Score  Match %  Relevance
1     John Doe          0.8934            89.34%   🟢 Highly Relevant
2     Jane Smith        0.7654            76.54%   🟡 Relevant
3     Bob Johnson       0.6234            62.34%   🟡 Relevant
```

---

## 🔐 Security Considerations

- File uploads are processed in-memory (not stored permanently)
- Use HTTPS in production
- Implement authentication for API endpoints
- Validate file types and sizes
- Store credentials in environment variables

---

## 🚢 Deployment

### Local Development
See `SETUP_GUIDE.md` for detailed local setup

### Azure Deployment
See `DEPLOYMENT.md` for cloud deployment instructions

### Docker Deployment
```bash
# Build Docker image
docker build -t resume-screening .

# Run container
docker run -p 8000:8000 -p 8501:8501 resume-screening
```

---

## 📈 Performance Metrics

### Typical Performance
- **Text Extraction**: ~100ms per document
- **Embedding Generation**: ~200ms per document
- **Similarity Calculation**: ~1ms per comparison
- **Total Time for 10 Resumes**: ~3-5 seconds

### Comparison Metrics
| Metric | Traditional ATS | This System |
|--------|-----------------|-------------|
| Keyword Dependency | High | Low |
| Semantic Understanding | No | Yes |
| Processing Speed | Fast | Very Fast |
| Bias Detection | Limited | Potential |
| Scalability | Moderate | High |

---

## 🔄 Future Enhancements

- [ ] Bias detection and mitigation
- [ ] Skill gap analysis
- [ ] Interview question generation
- [ ] Multi-language resume support
- [ ] LinkedIn integration
- [ ] Explainable AI (XAI) layer
- [ ] Database integration for resume history
- [ ] Machine learning model training with labeled data

---

## 🐛 Troubleshooting

### API won't start
```bash
# Check if port 8000 is available
netstat -ano | findstr :8000  # Windows
lsof -i :8000                # macOS/Linux

# Try different port
PORT=8001 python -m backend.main
```

### Streamlit connection error
```bash
# Edit frontend/app.py and change API URL:
api_url = "http://localhost:8000"  # Correct the URL
```

### Out of memory error
- Reduce number of resumes processed at once
- Use a lighter embedding model
- Increase available RAM

---

## 📚 References

- [Sentence Transformers Documentation](https://www.sbert.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [BERT Paper](https://arxiv.org/abs/1810.04805)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

---

## 📄 License

This project is provided for educational purposes.

---

## 👥 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

---

## ❓ FAQ

**Q: Can I use this for production recruitment?**
A: Yes, but add authentication, audit logging, and bias detection features.

**Q: How do I improve accuracy?**
A: Use better embedding models (all-mpnet-base-v2) or fine-tune with your data.

**Q: Can I integrate with my HR system?**
A: Yes, the REST API can be integrated with any system via HTTP requests.

**Q: How many resumes can it process?**
A: Limited by available RAM. Typically 100-1000 resumes per batch.

---

## 📞 Support

For questions or issues, please refer to the documentation files or open an issue on the project repository.

**Project Created For:** BTech/BCA Mini Project (2-3 Year Students)
**Last Updated:** February 2024
