# QuantumQR - Cloud Deployment Guide

Deploy this application to any cloud platform - completely free!

## 🌐 Quick Deploy Options

### Option 1: Render (Recommended - Easiest)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New Web Service"
4. Connect your GitHub repository
5. Settings:
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn quantumqr.wsgi`
6. Click "Deploy"

**Free tier includes:**

- 750 hours/month free
- PostgreSQL database
- SSL certificate

---

### Option 2: Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. In your project folder: `railway init`
4. Deploy: `railway up`

**Free tier includes:**

- $5 credit per month
- PostgreSQL
- Automatic SSL

---

### Option 3: Fly.io (Free + Fast)

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth signup`
3. Launch: `fly launch`
4. Deploy: `fly deploy`

**Free tier includes:**

- 3 shared VMs
- 3GB storage

---

### Option 4: PythonAnywhere (Simplest)

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create account (free tier available)
3. Upload your files
4. Configure WSGI file
5. Reload web app

**Free tier includes:**

- Always-on app
- Custom domain

---

## 🚀 Heroku Deployment

### Prerequisites

```bash
pip install gunicorn
pip install whitenoise
```

### Steps

1. **Create Heroku account**: https://heroku.com
2. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
3. **Login**: `heroku login`
4. **Create app**: `heroku create quantumqr`
5. **Add Postgres**: `heroku addons:create heroku-postgresql:hobby-dev`
6. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=True
   ```
7. **Deploy**: `git push heroku main`
8. **Run migrations**: `heroku run python manage.py migrate`
9. **Create superuser**: `heroku run python manage.py createsuperuser`

### Access your app

```bash
heroku open
```

---

## ⚙️ Environment Variables

Set these in your cloud platform:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False  # Use True only for development
ALLOWED_HOSTS=your-app.onrender.com,your-custom-domain.com
DATABASE_URL=postgresql://...  # Auto-provided by platforms
```

---

## 📁 Files Added for Deployment

- `Procfile` - Heroku process configuration
- `runtime.txt` - Python version
- `app.json` - Heroku app configuration
- `render.yaml` - Render configuration
- `railway.json` - Railway configuration

---

## 🔧 Quick Setup

After deploying to any platform:

1. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

2. **Create superuser**:

   ```bash
   python manage.py createsuperuser
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

---

## 🌍 Your App Will Be Live At

After deployment, your app will be accessible at:

- Render: `https://your-app.onrender.com`
- Railway: `https://your-app.railway.app`
- Fly: `https://your-app.fly.dev`
- Heroku: `https://your-app.herokuapp.com`

**Dynamic QR codes will now work worldwide!** 🌎

---

## 💡 Tips

1. **Free Hosting**: All platforms offer free tiers
2. **Database**: Most platforms auto-provision PostgreSQL
3. **SSL**: Automatic HTTPS certificates
4. **Custom Domain**: Add your own domain name
5. **Environment**: Change `DEBUG` to `False` for production

---

## 🎉 That's It!

Your QR code generator will work everywhere - no localhost, no IP addresses needed!

Anyone can:

- Scan QR codes from anywhere in the world
- Access your application 24/7
- Use dynamic QR codes with any URL
