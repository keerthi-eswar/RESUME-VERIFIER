# Detailed Setup Guide

## Complete Step-by-Step Installation

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB free space for dependencies
- **Internet**: Required for downloading models

---

## Installation Steps

### Step 1: Install Python

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click Install

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Step 2: Download Project

**Option A: Using Git**
```bash
git clone <repository-url>
cd resume-screening-system
```

**Option B: Manual Download**
1. Download as ZIP from repository
2. Extract files
3. Open terminal in project folder

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (Backend)
- Streamlit (Frontend)
- Sentence Transformers (ML models)
- Document processing libraries
- And 20+ other packages

Wait for installation to complete (~5-10 minutes depending on internet speed).

### Step 6: Configure Environment

```bash
# Copy the example configuration
cp .env.example .env
```

Edit `.env` file (optional, defaults work for basic usage):
```
PORT=8000
EMBEDDING_MODEL=all-MiniLM-L6-v2
DEBUG=False
```

### Step 7: Download ML Models

The first time you run the system, it will download embedding models (~200MB):

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Running the System

### Terminal 1: Start Backend API

```bash
# Make sure you're in the project directory and venv is activated
python -m backend.main
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Press CTRL+C to quit
```

### Terminal 2: Start Frontend

```bash
# Open a new terminal, navigate to project, activate venv
streamlit run frontend/app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## Access the Application

Open your web browser and go to:
```
http://localhost:8501
```

You should see the Resume Screening interface.

---

## Testing the System

### Using Sample Data

1. Go to `sample_data/` folder
2. Copy content from `sample_job_description.txt`
3. Paste in "Job Description" field
4. Upload `sample_resume.txt` (rename to `.pdf` or convert)
5. Click "Screen Resumes"

### Expected Result
You should see the resume ranked with a similarity score.

---

## Troubleshooting

### Issue: Port 8000 already in use

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000

# Kill process or use different port
PORT=8001 python -m backend.main
```

### Issue: Module not found errors

**Solution:**
```bash
# Verify venv is activated (should see (venv) in prompt)
which python  # Should show venv path

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### Issue: "ModuleNotFoundError: No module named 'sentence_transformers'"

**Solution:**
```bash
pip install sentence-transformers
```

### Issue: Streamlit won't connect to API

**Solution:**
1. Verify backend is running (check if API response at http://localhost:8000)
2. Check API URL in Streamlit sidebar: should be `http://localhost:8000`
3. Check firewall settings

### Issue: Models download very slowly

**Solution:**
```bash
# Download models manually to cache directory
export HF_HOME=./models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Project Verification

### Verify Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "api": "online",
    "embedding_service": "online"
  }
}
```

### Verify Files
Check that all required files exist:
```bash
backend/main.py
backend/document_processor.py
backend/embedding_generator.py
backend/similarity_calculator.py
frontend/app.py
requirements.txt
.env
README.md
```

---

## Optional: Azure OpenAI Setup (Production)

### Prerequisites
- Azure account
- Azure OpenAI service deployed
- API key and endpoint

### Setup Steps

1. Get credentials from Azure Portal:
   - Resource Name
   - API Key
   - Endpoint URL
   - Deployment Name

2. Update `.env` file:
```env
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=text-embedding-ada-002
```

3. Update `backend/embedding_generator.py`:
```python
# Uncomment Azure OpenAI class
# Comment out SentenceTransformer class
```

4. Restart backend

---

## Performance Optimization

### For Faster Processing

1. **Use Better Embeddings**
```env
EMBEDDING_MODEL=all-mpnet-base-v2
```

2. **Batch Processing**
```python
# Edit similarity_calculator.py
batch_size = 32  # Process 32 resumes at once
```

3. **Caching**
```python
# Add Redis caching for repeated JD analysis
```

---

## Development Tips

### Adding New Features

1. **New API Endpoint**
   - Edit `backend/main.py`
   - Add route method
   - Update models in `backend/models.py`

2. **Modify Frontend**
   - Edit `frontend/app.py`
   - Streamlit automatically reloads on save

3. **Change ML Model**
   - Edit `embedding_generator.py`
   - Update `EMBEDDING_MODEL` in `.env`

### Debugging

**Enable Debug Mode**
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

**Check Logs**
```bash
# Backend logs show in terminal
# Frontend logs show in Streamlit sidebar
```

---

## Now You're Ready!

Your Resume Screening System is ready to use.

**Next Steps:**
1. Upload sample resumes
2. Test with different job descriptions
3. Evaluate accuracy with your own data
4. Consider enhancements from Future Scope
5. Deploy to cloud if needed (see DEPLOYMENT.md)

---

## Getting Help

- Check `README.md` for overview
- Check `DEPLOYMENT.md` for cloud setup
- Review code comments in source files
- Check Streamlit/FastAPI documentation online

**Happy screening! 🎓**
