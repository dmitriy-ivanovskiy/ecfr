# Deployment Instructions for Render

## Prerequisites
- GitHub repository with your code
- Render account (free)

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Fix Render deployment configuration"
git push origin main
```

### 2. Deploy on Render

1. **Go to [Render Dashboard](https://render.com/)**
2. **Click "New +" → "Blueprint"**
3. **Connect your GitHub repository**
4. **Render will automatically detect `render.yaml`**
5. **Click "Apply"**

### 3. Update Frontend Configuration

After deployment, update `frontend/config.js` with your actual backend URL:

```javascript
API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? "http://127.0.0.1:8001"
    : "https://YOUR-BACKEND-NAME.onrender.com", // Replace with actual URL
```

### 4. Your Deployed URLs

- **Frontend**: `https://ecfr-frontend.onrender.com`
- **Backend API**: `https://ecfr-backend.onrender.com`

## Configuration Files

The deployment uses these key files:
- **`requirements.txt`** (root) - Python dependencies
- **`start.py`** (root) - Production startup script
- **`render.yaml`** - Deployment configuration

## Important Notes

- **Free tier limitations**: Service sleeps after 15 minutes of inactivity
- **Cold start**: First request after sleep may take 30+ seconds
- **External API**: Your app fetches data from ecfr.gov (allowed)
- **Health check**: Available at `/health` endpoint

## Local Development

To continue local development:
```bash
./start.sh
```

## Monitoring

- Check deployment status in Render dashboard
- View logs in Render for debugging
- Test health endpoint: `https://your-backend.onrender.com/health` 