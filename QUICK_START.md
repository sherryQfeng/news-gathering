# 🚀 Quick Start Guide

## 🏃‍♂️ Super Fast Setup (2 minutes!)

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Start your news hub:**
   ```bash
   ./start.sh
   ```
   
   *OR manually:*
   ```bash
   source .venv/bin/activate
   python run.py
   ```

3. **Open your browser:**
   ```
   http://localhost:8000
   ```

That's it! 🎉

## 📧 Want Email Digests? (Optional)

1. **Edit your email settings:**
   ```bash
   nano .env
   ```

2. **For Gmail users:**
   - Enable 2FA on your Google account
   - Create an "App Password"
   - Use these settings:
     ```
     SMTP_HOST=smtp.gmail.com
     SMTP_PORT=587
     SMTP_USERNAME=your.email@gmail.com
     SMTP_PASSWORD=your-16-character-app-password
     TO_EMAIL=your.email@gmail.com
     ```

## 🎮 Cool Features to Try

- **Press `1`** to switch to AI news
- **Press `2`** to switch to Economics/Politics  
- **Click the villager avatar** for surprises!
- **Click "Refresh News"** to get latest articles
- **Click "Send Digest"** to email yourself now

## 🔧 Customize Your Feeds

Edit `config.yaml` to add your favorite RSS feeds:

```yaml
feeds:
  ai_frontier:
    - name: "Your Favorite AI Blog 🤖"
      url: "https://yourblog.com/rss"
```

## ❓ Need Help?

- **No articles showing?** Try refreshing feeds manually
- **Email not working?** Check your `.env` file settings  
- **Something broken?** Check the console for error messages

---

🦝 **Tom Nook says:** "Thanks for choosing Animal Crossing News Hub!" 🌟
