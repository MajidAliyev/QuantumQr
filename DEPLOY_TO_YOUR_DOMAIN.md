# 🚀 Deploy QuantumQR to qrcodebymajid.work.gd

Complete step-by-step guide to deploy your QR code generator to your custom domain.

## 📋 Prerequisites

- [ ] GitHub account (free)
- [ ] Render.com account (free)
- [ ] Your domain: qrcodebymajid.work.gd (already have ✅)

---

## Step 1: Push Code to GitHub (5 minutes)

### 1.1 Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `quantumqr`
3. Description: "Dynamic QR Code Generator with Analytics"
4. Make it **Public** (or Private if you prefer)
5. Click "Create repository"

### 1.2 Push Your Code

Open terminal in your project folder and run:

```bash
cd "/Users/majid/Desktop/QR Code Generator"

# Initialize Git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "QuantumQR - Ready for deployment"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/quantumqr.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 2: Deploy to Render.com (5 minutes)

### 2.1 Create Render Account

1. Go to: https://render.com
2. Click "Sign up for free"
3. Choose "Sign up with GitHub"
4. Authorize Render to access GitHub

### 2.2 Create Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect GitHub"
4. Find your `quantumqr` repository
5. Click "Connect"

### 2.3 Configure Service

**Basic Settings:**

- **Name**: `quantumqr` (or any name you want)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Runtime**: `Python 3`

**Build & Deploy:**

- **Build Command**:

  ```bash
  pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
  ```

- **Start Command**:
  ```bash
  gunicorn quantumqr.wsgi
  ```

**Plan:**

- Select **Free** tier
- Click "Create Web Service"

### 2.4 Add Environment Variables

1. While it's deploying, click on "Environment" tab
2. Add these variables:

   ```
   Name: SECRET_KEY
   Value: [Click "Generate" or use the one generated below]
   ```

   ```bash
   # Run this to generate a secret key:
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

   Add another variable:

   ```
   Name: DEBUG
   Value: False
   ```

3. Click "Save Changes"

### 2.5 Wait for Deployment

- Render will build and deploy (takes 3-5 minutes)
- You'll see logs in real-time
- When done, you'll have a URL like: `https://quantumqr.onrender.com`

✅ **Your app is now live on Render!**

---

## Step 3: Point Your Domain to Render (10 minutes)

### 3.1 Get DNS Settings from Render

1. In Render dashboard, go to your service
2. Click on **"Settings"** tab
3. Scroll down to **"Custom Domains"**
4. Click **"Add Custom Domain"**
5. Enter: `qrcodebymajid.work.gd`
6. Click "Create"

### 3.2 Render Will Show DNS Instructions

You'll see something like:

```
Add these DNS records at your domain provider:
- Type: CNAME
- Name: @
- Value: your-service.onrender.com
```

### 3.3 Update DNS at DNSExit.com

1. Login to: https://www.dnsexit.com
2. Go to **"DNS Management"**
3. Find your domain: `qrcodebymajid.work.gd`
4. Add/Update DNS records:

   **Record 1:**

   ```
   Type: CNAME
   Name: @
   Value: your-service.onrender.com (from Render)
   TTL: 3600
   ```

   **Record 2:**

   ```
   Type: A
   Name: www
   Value: [Render's IP address - get from Render]
   TTL: 3600
   ```

5. Click "Save" or "Update"

### 3.4 Wait for DNS Propagation

- DNS updates take 5-15 minutes
- You can check status in Render dashboard

---

## Step 4: Create Admin User (Optional)

Once your app is live, create a superuser:

1. In Render dashboard, click "Shell"
2. Run:

```bash
python manage.py createsuperuser
```

3. Follow prompts to create admin user

Or access Django admin at:

- `https://qrcodebymajid.work.gd/admin`

---

## Step 5: Test Your Deployment! 🎉

### 5.1 Access Your App

Go to: **https://qrcodebymajid.work.gd**

### 5.2 Test Features

1. **Register** a new account
2. **Create a dynamic QR code**
3. **Check the URL** - it should use your domain!
4. **Scan with phone** - should work worldwide!

### 5.3 Create Your First QR

1. Login
2. Go to "Create QR Code"
3. Create a dynamic QR
4. The short URL will be:
   ```
   https://qrcodebymajid.work.gd/redirect/xxxxx/
   ```
5. Scan it - works anywhere in the world! 🌍

---

## ✅ You're Done!

Your QR code generator is now:

- ✅ Live at: **https://qrcodebymajid.work.gd**
- ✅ Accessible worldwide
- ✅ Using professional domain
- ✅ HTTPS/SSL automatic
- ✅ Running 24/7 (on free tier)
- ✅ PostgreSQL database included

---

## 📊 What You Get

### Free Tier on Render:

- **750 hours/month** (31 days free)
- **Always online** (spins down after 15 min inactivity)
- **PostgreSQL database** included
- **SSL certificate** automatic
- **Custom domain** support

### Upgrading (if needed):

- **$7/month**: Always on, no spin down
- More resources
- Faster deployment

---

## 🔧 Troubleshooting

### DNS Not Working?

- Wait 15-30 minutes after updating DNS
- Check DNS propagation: https://dnschecker.org
- Verify records are correct in Render dashboard

### Build Fails?

- Check logs in Render dashboard
- Make sure all dependencies in requirements.txt
- Secret key is set correctly

### Can't Access App?

- Check ALLOWED_HOSTS in settings.py
- Verify domain is added in Render
- Check Render logs for errors

---

## 🎯 Your QR Codes Now Use:

**Before:** `http://localhost:8080/redirect/xxxxx/`

**After:** `https://qrcodebymajid.work.gd/redirect/xxxxx/`

**Professional, worldwide, 24/7!** 🚀

---

## 📞 Need Help?

- **Render Support**: Very responsive, great documentation
- **Django Docs**: https://docs.djangoproject.com
- **Render Docs**: https://render.com/docs

---

**Congratulations! Your QR code generator is now deployed to your custom domain!** 🎉
