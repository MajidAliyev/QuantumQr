# Custom Domain Setup - qrcodebymajid.work.gd

You have a custom domain **qrcodebymajid.work.gd**! Here's how to use it.

## 🌐 Option 1: Point Your Domain to a Cloud Service

### Render.com with Custom Domain

1. Deploy your app to Render: https://render.com
2. Your app will be at: `https://your-app.onrender.com`
3. Go to your Render dashboard → Settings
4. Add Custom Domain: `qrcodebymajid.work.gd`
5. Render will give you DNS records to add
6. Update your DNS at DNSExit.com with Render's records

### The IP Update Script

The `ipupdate.sh` script keeps your domain's IP updated when running locally.

## 📝 To Use Your Custom Domain Locally:

### Step 1: Run Your Django App

```bash
cd "/Users/majid/Desktop/QR Code Generator"
source venv/bin/activate
python manage.py runserver 0.0.0.0:8080
```

### Step 2: Set Up Dynamic DNS Updates

The script `ipupdate.sh` will:

- Update your domain's IP every 12 minutes
- Keep your domain pointing to your current public IP
- Allow remote access to your local server

### Step 3: Run the IP Update Script

```bash
cd "/Users/majid/Desktop/QR Code Generator"
./ipupdate.sh
```

This will:

1. Add a cron job that runs every 12 minutes
2. Update `qrcodebymajid.work.gd` to point to your current IP
3. Log results to `/var/log/ipupdate.log`

### Step 4: Update Django Settings

Update `quantumqr/settings.py`:

```python
ALLOWED_HOSTS = ['qrcodebymajid.work.gd', 'localhost', '127.0.0.1']
```

### Step 5: Test Your Domain

Once DNS updates (usually 5-10 minutes), your app will be accessible at:

- **https://qrcodebymajid.work.gd:8080**
- Your QR codes will use this domain!

## 🎯 Better Option: Deploy to Cloud + Use Your Domain

**Recommended approach:**

1. **Deploy to Render.com** (or Railway/Fly.io):

   - Your app gets a free subdomain: `quantumqr.onrender.com`
   - It's always online, no need for your computer
   - Professional and reliable

2. **Point Your Custom Domain**:

   - Add `qrcodebymajid.work.gd` in Render dashboard
   - Render gives you DNS records
   - Update DNS at DNSExit.com

3. **Result**:
   - Your app is at: `https://qrcodebymajid.work.gd`
   - Works 24/7 worldwide
   - No localhost, no IP management
   - Professional domain with SSL

## 🔧 DNSExit.com Settings

To point your domain to a cloud service:

1. Login to: https://www.dnsexit.com
2. Go to DNS Management
3. Add these records (Render will provide exact values):
   - Type: A
   - Name: @
   - Value: Render's IP address
   - TTL: 3600

Or for CNAME:

- Type: CNAME
- Name: @
- Value: your-app.onrender.com
- TTL: 3600

## 📊 Current Setup

Your domain: **qrcodebymajid.work.gd**

You can use it in two ways:

1. **Local Dynamic DNS**: Update IP every 12 min with the script
2. **Cloud Hosting**: Point domain to Render/Railway (recommended)

## 🚀 Quick Start

### For Local Testing (using Dynamic DNS):

```bash
# Run the app
python manage.py runserver 0.0.0.0:8080

# In another terminal, set up auto IP updates
./ipupdate.sh

# Check crontab
crontab -l

# Your app will be at: http://qrcodebymajid.work.gd:8080
```

### For Production (recommended):

1. Deploy to Render.com
2. Add custom domain in Render dashboard
3. Update DNS records at DNSExit
4. Wait 5-10 minutes for propagation
5. Done! Your app is at **https://qrcodebymajid.work.gd**

## ⚠️ Important Notes

- The dynamic DNS script updates every 12 minutes (minimum interval)
- Your computer needs to be on and running
- If your IP changes, it will auto-update in ~12 minutes
- For 24/7 uptime, cloud hosting is recommended

## 🎉 What You Get

With your custom domain, QR codes will use:

- **`https://qrcodebymajid.work.gd/redirect/xxxxx/`**
- Professional, branded URLs
- Works worldwide
- No localhost, no IPs

Choose the approach that works best for you!
