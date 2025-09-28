# 🌟 Animal Crossing News Hub 🌟

> *A whimsical daily news aggregator that brings you AI frontier updates and economics/politics news with the charm of Animal Crossing! 🏝️*

![Animal Crossing Style](https://img.shields.io/badge/Style-Animal%20Crossing-brightgreen?style=for-the-badge&logo=nintendo-switch)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey?style=for-the-badge&logo=flask)

## 🦝 What Tom Nook Built For You

A cozy, retro-styled news website that:
- 📡 **Aggregates RSS feeds** from top AI and economics sources
- 🎨 **Beautiful Windows 98/Animal Crossing UI** with whimsical styling
- 📧 **Daily email digest** sent to your inbox every morning
- 🔄 **Automatic updates** twice daily (6 AM & 6 PM)
- 💬 **Villager comments** - each article gets a fun comment from Animal Crossing characters
- 📊 **Statistics dashboard** to track your news consumption
- 🌟 **Completely customizable** RSS feed sources

## 🏠 Quick Start (The Easy Way)

1. **Clone this cozy repository:**
   ```bash
   git clone <your-repo-url>
   cd news-gathering
   ```

2. **Set up your environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your email (optional but recommended):**
   ```bash
   cp .env.example .env
   # Edit .env with your email settings
   ```

4. **Run the magical setup script:**
   ```bash
   python run.py
   ```

That's it! 🎉 Your news hub will be running at `http://localhost:8000`

## 📧 Email Setup Guide

### For Gmail Users:
1. Enable 2-factor authentication on your Google account
2. Generate an "App Password" for this application
3. Use these settings in your `.env` file:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your.email@gmail.com
   SMTP_PASSWORD=your-16-character-app-password
   FROM_EMAIL="Animal Crossing News 🌟 <your.email@gmail.com>"
   TO_EMAIL=your.email@gmail.com
   ```

### For Other Email Providers:
- **Outlook/Hotmail:** `smtp-mail.outlook.com`, port `587`
- **Yahoo:** `smtp.mail.yahoo.com`, port `587`
- **Custom SMTP:** Use your provider's SMTP settings

## 🎮 Features & Easter Eggs

### 🌟 Main Features:
- **Tab-based news browsing** (AI vs Economics/Politics)
- **Real-time feed refresh** with progress indicators
- **Mobile-responsive design** for reading on any device
- **Keyboard shortcuts** (Press `1` for AI, `2` for Economics)
- **Click the villager avatar** for surprise messages!

### 🦉 Villager Comments:
Each article gets a whimsical comment from characters like:
- 🦝 Tom Nook (business insights)
- 🐕 Isabelle (helpful observations)
- 🦉 Blathers (scientific wonderment)
- 🎵 K.K. Slider (creative takes)
- ⭐ Celeste (philosophical thoughts)

## 🔧 Customization

### Adding New RSS Feeds:
Edit `config.yaml` to add your favorite news sources:

```yaml
feeds:
  ai_frontier:
    - name: "Your AI Blog 🤖"
      url: "https://yourblog.com/rss"
  
  economics_politics:
    - name: "Economic Times 💰"
      url: "https://economictimes.com/rss"
```

### Changing Colors:
Modify the CSS variables in `static/style.css`:

```css
:root {
    --sage-green: #8FBC8F;      /* Primary color */
    --light-pink: #FFB6C1;      /* Accent color */
    --cream-beige: #F5F5DC;     /* Background */
    /* ... more colors ... */
}
```

## 🚀 Deployment Options

### Option 1: Local Cron (Recommended)
The app includes automatic scheduling! Just run:
```bash
python app.py
```
Daily tasks run automatically at:
- **6 AM:** Morning news fetch
- **7 AM:** Email digest sent
- **6 PM:** Evening news update

### Option 2: Docker
```bash
docker build -t animal-crossing-news .
docker run -p 8000:8080 -v $(pwd)/data:/app/data animal-crossing-news
```

### Option 3: Cloud Deployment
Deploy to platforms like:
- **Heroku:** Simple git-based deployment
- **Railway:** Modern, developer-friendly
- **Fly.io:** Global edge deployment
- **DigitalOcean App Platform:** Managed containers

## 📊 API Endpoints

- `GET /` - Main news interface
- `GET /refresh` - Manually refresh all feeds
- `GET /send-digest` - Send email digest now
- `GET /stats` - View statistics JSON

## 🐛 Troubleshooting

### Common Issues:

**"No articles showing up"**
- Check your internet connection
- Some RSS feeds might be temporarily unavailable
- Try refreshing feeds manually

**"Email not sending"**
- Verify your `.env` file settings
- For Gmail, make sure you're using an App Password
- Check spam/junk folder

**"Database errors"**
- The SQLite database is created automatically
- If issues persist, delete `animal_crossing_news.db` and restart

### Getting Help:
- Check the browser console for error messages
- Look at the terminal output for server errors
- RSS feed URLs sometimes change - update `config.yaml` if needed

## 🌟 Technical Details

### Built With Love Using:
- **Python 3.11+** - The programming language
- **Flask** - Web framework for the UI
- **SQLAlchemy** - Database management
- **APScheduler** - Automated daily tasks
- **Feedparser** - RSS feed parsing
- **98.css** - Retro Windows 98 styling
- **Custom CSS** - Animal Crossing-inspired design

### Architecture:
```
├── app.py              # Main Flask application
├── models.py           # Database models
├── fetch.py            # RSS feed fetcher
├── emailer.py          # Email digest system
├── config.yaml         # RSS feed configuration
├── templates/          # HTML templates
├── static/             # CSS and JavaScript
└── run.py             # Setup and launch script
```

## 🎯 Perfect For:

- 🎓 **Economics PhD students** who want focused, relevant news
- 🤖 **AI enthusiasts** tracking the latest developments
- 🎮 **Animal Crossing fans** who love whimsical design
- 📰 **Anyone tired of cluttered news websites**
- 💌 **People who prefer email digests** over social media

## 🌈 Future Ideas

Want to contribute? Here are some fun ideas:
- 🧠 AI-powered article summarization
- 🔔 Browser notifications for breaking news
- 🎨 More villager characters and comments
- 📱 Mobile app version
- 🌍 Multi-language support
- 🎵 Background music toggle (K.K. Slider tunes!)

## 📜 License

This project is open source and available under the MIT License. Tom Nook approves! 🦝

---

*Built with 🌟 and inspired by the cozy world of Animal Crossing. Happy news reading! 🏝️*
