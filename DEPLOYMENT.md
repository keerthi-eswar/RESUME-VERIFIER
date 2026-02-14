# Deployment Guide for Production

## Cloud Deployment Options

This guide covers deploying the Resume Screening System to Azure, AWS, or other cloud platforms.

---

## Option 1: Microsoft Azure Deployment

### Architecture
```
Internet → Azure App Service (Frontend) ↓
           ↓ (API Calls) ↓
Azure App Service (Backend API) → Azure OpenAI Service
                                ↓
                        Azure ML Endpoint (Optional)
```

### Prerequisites
- Azure subscription
- Azure CLI installed
- Docker installed (optional)

### Step-by-Step Deployment

#### 1. Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name "resume-screening-rg" --location "eastus"

# Create App Service Plan
az appservice plan create \
  --name "resume-screening-plan" \
  --resource-group "resume-screening-rg" \
  --sku "B2" \
  --is-linux
```

#### 2. Deploy Backend API

**Option A: Git Automatic Deployment**

```bash
# Create web app
az webapp create \
  --resource-group "resume-screening-rg" \
  --plan "resume-screening-plan" \
  --name "resume-screening-api" \
  --runtime "PYTHON:3.11"

# Set environment variables
az webapp config appsettings set \
  --resource-group "resume-screening-rg" \
  --name "resume-screening-api" \
  --settings \
    PORT=8000 \
    EMBEDDING_MODEL=all-MiniLM-L6-v2 \
    AZURE_OPENAI_KEY="your-key" \
    AZURE_OPENAI_ENDPOINT="your-endpoint"

# Deploy code
cd backend
az webapp deployment source config-zip \
  --resource-group "resume-screening-rg" \
  --name "resume-screening-api" \
  --src-path backend.zip
```

**Option B: Docker Deployment**

Create `Dockerfile` in project root:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "backend.main"]
```

Deploy Docker image:
```bash
# Build image
docker build -t resume-screening-api .

# Create container registry
az acr create \
  --resource-group "resume-screening-rg" \
  --name "screeningregistry" \
  --sku Basic

# Push image
docker tag resume-screening-api screeningregistry.azurecr.io/resume-screening-api
docker push screeningregistry.azurecr.io/resume-screening-api

# Deploy from container
az webapp create \
  --resource-group "resume-screening-rg" \
  --plan "resume-screening-plan" \
  --name "resume-screening-api" \
  --deployment-container-image-name screeningregistry.azurecr.io/resume-screening-api
```

#### 3. Deploy Frontend

Create separate App Service for Streamlit:
```bash
az webapp create \
  --resource-group "resume-screening-rg" \
  --plan "resume-screening-plan" \
  --name "resume-screening-ui" \
  --runtime "PYTHON:3.11"

# Set API URL for frontend
az webapp config appsettings set \
  --resource-group "resume-screening-rg" \
  --name "resume-screening-ui" \
  --settings API_URL="https://resume-screening-api.azurewebsites.net"
```

#### 4. Configure Azure OpenAI Integration

```bash
# Update backend with Azure OpenAI credentials
az webapp config appsettings set \
  --resource-group "resume-screening-rg" \
  --name "resume-screening-api" \
  --settings \
    AZURE_OPENAI_KEY="your-api-key" \
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
    AZURE_OPENAI_DEPLOYMENT="text-embedding-ada-002"
```

---

## Option 2: AWS Deployment

### Architecture
```
CloudFront (CDN) → EC2 (Frontend - Streamlit)
                   ↓ (API Calls) ↓
                   EC2 (Backend - FastAPI)
                   ↓
                   OpenAI API (or SageMaker)
```

### Prerequisites
- AWS account
- AWS CLI configured
- EC2 key pair created

### Deployment Steps

#### 1. Create EC2 Instances

**For Backend:**
```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-groups backend-sg

# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Setup backend
cd /home/ec2-user
git clone <repo-url>
cd resume-screening-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m backend.main
```

**For Frontend:**
```bash
# Similar setup for frontend
streamlit run frontend/app.py \
  --server.address=0.0.0.0 \
  --server.port=8501
```

#### 2. Create RDS Database (Optional)

```bash
aws rds create-db-instance \
  --db-instance-identifier resume-screening-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20
```

#### 3. Setup Load Balancer

```bash
# Create Application Load Balancer
aws elbv2 create-load-balancer \
  --name resume-screening-alb \
  --subnets subnet-12345 subnet-67890 \
  --scheme internet-facing
```

#### 4. Configure Security Groups

```bash
# Backend security group
aws ec2 create-security-group \
  --group-name backend-sg \
  --description "Backend security group"

# Allow API traffic
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0
```

---

## Option 3: Google Cloud Platform (GCP)

### Quick Deployment

```bash
# Initialize GCP project
gcloud init

# Create Cloud Run services
# For Backend
gcloud run deploy resume-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars PORT=8000

# For Frontend
gcloud run deploy resume-ui \
  --source frontend/ \
  --platform managed \
  --region us-central1 \
  --set-env-vars API_URL=https://resume-api-url.run.app
```

---

## Option 4: Heroku Deployment (Easiest)

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create resume-screening

# Add buildpack for Python
heroku buildpacks:add heroku/python

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Set environment variables
heroku config:set EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## Docker Compose for Local/Production

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      PORT: 8000
      EMBEDDING_MODEL: all-MiniLM-L6-v2
    volumes:
      - ./backend:/app/backend

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    environment:
      API_URL: http://backend:8000
    depends_on:
      - backend

volumes:
  data:
```

Run with:
```bash
docker-compose up
```

---

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: pytest

    - name: Deploy to Azure
      uses: azure/CLI@v1
      with:
        inlineScript: |
          az login --service-principal
          az webapp deployment source config-zip \
            --resource-group resume-screening-rg \
            --name resume-screening-api \
            --src-path budget.zip
```

---

## Scale Deployment

### For High Traffic

```bash
# Azure - Scale up App Service
az appservice plan update \
  --name "resume-screening-plan" \
  --resource-group "resume-screening-rg" \
  --sku "P1V2"

# Add auto-scaling
az monitor autoscale create \
  --resource-group "resume-screening-rg" \
  --resource-name "resume-screening-plan" \
  --resource-type "Microsoft.Web/serverfarms" \
  --min-count 2 \
  --max-count 10 \
  --count 3
```

---

## Security Best Practices

1. **Environment Variables**
   ```bash
   # Never commit credentials
   # Use managed identities or secrets manager
   ```

2. **SSL/TLS**
   ```bash
   # Enable HTTPS for all endpoints
   # Use Azure App Service certificates
   ```

3. **Authentication**
   ```python
   # Add API key validation
   # Implement rate limiting
   ```

4. **Logging & Monitoring**
   ```bash
   # Enable Application Insights
   # Monitor API performance
   # Alert on errors
   ```

---

## Post-Deployment Checklist

- [ ] API endpoint is accessible from web
- [ ] Frontend connects to API successfully
- [ ] File uploads work correctly
- [ ] Similarity calculations execute without errors
- [ ] Results display properly
- [ ] Logs are being collected
- [ ] Monitoring is enabled
- [ ] SSL certificate is valid
- [ ] Backups are configured
- [ ] Disaster recovery plan is in place

---

## Monitoring & Maintenance

### Health Checks
```bash
# Monitor API health
curl https://your-api-url/health

# Check logs
# Azure
az webapp log tail --name resume-screening-api

# AWS CloudWatch
aws logs tail /aws/ec2/resume-screening --follow
```

### Update Models
```bash
# Deploy new embedding models
# Update EMBEDDING_MODEL environment variable
# Restart application
```

---

## Cost Estimation

### Azure
- App Service: $10-20/month
- OpenAI API: Pay per token (~$0.02 per 1K embeddings)
- Storage: ~$1/month

### AWS
- EC2 t3.medium: ~$30/month
- RDS (if needed): ~$15/month
- Data transfer: Minimal

### GCP
- Cloud Run: Pay per invocation (~$0.0000002 per call)
- Cloud Storage: ~$0.020 per GB

---

## Getting Production Ready

1. **Test thoroughly** before deploying
2. **Setup monitoring** for early issue detection
3. **Configure backups** for data safety
4. **Implement authentication** for access control
5. **Use CDN** for static content (if needed)
6. **Monitor costs** closely
7. **Document deployment** process
8. **Setup alerts** for critical issues

---

## Need Help?

- Check cloud provider documentation
- Review GitHub Actions workflows
- Consult logging for error messages
- Check Official FastAPI/Streamlit deployment guides

**Your system is now production-ready!** 🚀
