# 🚀 Deployment Guide - HealthPredict AI

## Option 1: Render (Recommended - Free)

### Step 1: Prepare Your Code
✅ All files are ready! You have:
- `app.py` - Flask backend
- `html.html` - Frontend
- `styles.css` - Styling
- `model.pkl` & `scaler.pkl` - Your trained ML model
- `requirements.txt` - Dependencies
- `Procfile` - Deployment config
- `font_files/` - Custom fonts

### Step 2: Deploy to Render
1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - HealthPredict AI"
   git branch -M main
   git remote add origin https://github.com/yourusername/healthpredict-ai.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name:** healthpredict-ai
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app.py`
   - Click "Deploy"

3. **Your app will be live at:** `https://healthpredict-ai-[random].onrender.com`

---

## Option 2: Heroku (Popular)

### Setup:
1. Install Heroku CLI
2. Create `runtime.txt`:
   ```
   python-3.9.16
   ```
3. Deploy:
   ```bash
   heroku create healthpredict-ai
   git push heroku main
   ```

---

## Option 3: Railway (Modern)

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo
3. Deploy automatically
4. Custom domain available

---

## Option 4: PythonAnywhere (Beginner-friendly)

1. Upload files to [pythonanywhere.com](https://pythonanywhere.com)
2. Set up web app with Flask
3. Configure WSGI file

---

## Option 5: DigitalOcean App Platform

1. Connect GitHub to [DigitalOcean](https://cloud.digitalocean.com/apps)
2. Auto-deploy from repo
3. $5/month for always-on

---

## 🎯 Recommended: Start with Render

**Why Render?**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Handles ML models well
- ✅ Custom domains
- ✅ SSL certificates included
- ✅ Good for portfolio projects

## 📝 After Deployment:

1. **Test your live app**
2. **Add to your portfolio**
3. **Share the link:**
   - LinkedIn
   - GitHub README
   - CV/Resume
   - Cambridge Spark showcase

## 🔧 Troubleshooting:

**If deployment fails:**
- Check build logs
- Ensure all files are committed
- Verify requirements.txt is complete
- Check Python version compatibility

**Performance tips:**
- Models load on startup (may take 30-60 seconds)
- First request might be slow (cold start)
- Consider upgrading to paid tier for better performance

Your ML health prediction app will be live and accessible to anyone worldwide! 🌍