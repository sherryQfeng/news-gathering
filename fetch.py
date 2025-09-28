import feedparser
import yaml
import datetime as dt
import html
import bleach
import random
from urllib.parse import urlparse
from models import SessionLocal, Article, init_db
from dateutil import parser as dtparse

# Allowed HTML tags for article summaries
ALLOWED_TAGS = ['b', 'i', 'em', 'strong', 'a', 'code', 'pre', 'p', 'ul', 'ol', 'li', 'br']

# Whimsical villager comments for different article types
VILLAGER_COMMENTS = {
    "ai_frontier": [
        "Wow! This reminds me of when Blathers explains science! 🦉",
        "Tom Nook says this could change how we do business! 💼",
        "K.K. Slider would totally write a song about this! 🎵",
        "Even Isabelle finds this fascinating! 🐕",
        "This is more complex than Redd's art authentication! 🎨",
        "Celeste would love to discuss this under the stars! ⭐"
    ],
    "economics_politics": [
        "Hmm, sounds like Turnip price predictions! 📈",
        "Tom Nook definitely needs to hear about this! 🦝",
        "This affects the whole island economy! 🏝️",
        "Even more complicated than Nook's Cranny pricing! 💰",
        "Isabelle would make an announcement about this! 📢",
        "This reminds me of the Great Turnip Crash of '21! 😱"
    ]
}

# Fun emojis for different article categories
CATEGORY_EMOJIS = {
    "ai_frontier": ["🤖", "🧠", "⚡", "🔬", "💻", "🚀", "🎯", "⭐"],
    "economics_politics": ["💰", "📈", "📊", "🏛️", "🗳️", "💼", "🌍", "📰"]
}

def load_config(path="config.yaml"):
    """Load configuration from YAML file"""
    with open(path, "r") as f:
        return yaml.safe_load(f)

def clean_summary(summary_text):
    """Clean and sanitize article summary"""
    if not summary_text:
        return ""
    
    # First, strip all HTML tags completely for a clean text-only summary
    import re
    # Remove all HTML tags
    cleaned = re.sub(r'<[^>]+>', '', summary_text)
    # Remove extra whitespace and newlines
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Decode HTML entities
    import html
    cleaned = html.unescape(cleaned)
    
    # Limit length to keep it digestible
    if len(cleaned) > 300:
        cleaned = cleaned[:297] + "..."
    return cleaned

def normalize_datetime(entry):
    """Try to extract and normalize datetime from feed entry"""
    for field in ("published", "updated"):
        if hasattr(entry, field) and getattr(entry, field):
            try:
                parsed_date = dtparse.parse(getattr(entry, field))
                # Convert to UTC and make timezone-naive for consistency
                if parsed_date.tzinfo is not None:
                    parsed_date = parsed_date.utctimetuple()
                    parsed_date = dt.datetime(*parsed_date[:6])
                return parsed_date
            except Exception:
                continue
    return dt.datetime.utcnow()

def is_recent_article(published_date, max_days_old=30):
    """Check if article is recent enough (default: within last 30 days)"""
    if not published_date:
        return False
    
    # Ensure both dates are timezone-naive for comparison
    cutoff_date = dt.datetime.utcnow() - dt.timedelta(days=max_days_old)
    
    # Make sure published_date is timezone-naive
    if hasattr(published_date, 'tzinfo') and published_date.tzinfo is not None:
        published_date = published_date.replace(tzinfo=None)
    
    return published_date >= cutoff_date

def get_villager_comment(category):
    """Get a random whimsical comment from our Animal Crossing villagers"""
    comments = VILLAGER_COMMENTS.get(category, ["Interesting news from the outside world! 🌟"])
    return random.choice(comments)

def get_category_emoji(category):
    """Get a random emoji for the article category"""
    emojis = CATEGORY_EMOJIS.get(category, ["📰"])
    return random.choice(emojis)

def fetch_feeds():
    """Fetch articles from all RSS feeds"""
    print("🌅 Good morning! Time to gather the daily news! (like collecting fruit!) 🍎")
    
    cfg = load_config()
    init_db()
    db = SessionLocal()
    added_count = 0
    
    try:
        for category, feeds in cfg.get("feeds", {}).items():
            print(f"📡 Fetching {category} news...")
            
            for feed_info in feeds:
                feed_name = feed_info["name"]
                feed_url = feed_info["url"]
                
                print(f"  🔍 Checking {feed_name}...")
                
                try:
                    # Parse the RSS feed
                    parsed_feed = feedparser.parse(feed_url)
                    
                    # Limit items per feed as configured
                    max_items = cfg["site"]["num_items_per_feed"]
                    entries = parsed_feed.entries[:max_items]
                    
                    for entry in entries:
                        # Skip entries without links
                        if not hasattr(entry, 'link') or not entry.link:
                            continue
                        
                        # Get the publication date
                        published_date = normalize_datetime(entry)
                        
                        # Skip articles older than 7 days to ensure fresh content
                        if not is_recent_article(published_date, max_days_old=7):
                            print(f"    ⏭️  Skipping old article: {getattr(entry, 'title', 'Untitled')[:50]}... ({published_date.strftime('%Y-%m-%d') if published_date else 'no date'})")
                            continue
                        
                        # Create article object
                        article = Article(
                            source=feed_name,
                            title=html.unescape(getattr(entry, "title", "Untitled Article")),
                            link=entry.link,
                            summary=clean_summary(getattr(entry, "summary", 
                                                  getattr(entry, "description", ""))),
                            published=published_date,
                            category=category,
                            emoji=get_category_emoji(category),
                            villager_comment=get_villager_comment(category)
                        )
                        
                        try:
                            db.add(article)
                            db.commit()
                            added_count += 1
                            print(f"    ✅ Added: {article.title[:50]}...")
                        except Exception as e:
                            # Likely a duplicate (unique constraint on link)
                            db.rollback()
                            print(f"    ⏭️  Skipped duplicate: {article.title[:30]}...")
                            
                except Exception as e:
                    print(f"    ❌ Error fetching {feed_name}: {e}")
                    continue
    
    finally:
        db.close()
    
    print(f"🎉 Finished! Added {added_count} new articles to our collection!")
    print("📅 All articles are guaranteed to be from the last 7 days!")
    if added_count == 0:
        print("💡 No new articles found - your database is already up to date with fresh content!")
    return added_count

if __name__ == "__main__":
    fetch_feeds()
