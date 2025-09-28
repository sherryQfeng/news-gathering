import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from models import init_db, SessionLocal, Article
from sqlalchemy import select, desc, func
from fetch import fetch_feeds
from emailer import send_digest
from apscheduler.schedulers.background import BackgroundScheduler
import random
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "animal-crossing-news-secret")

# Initialize database
init_db()

# Fun greetings and messages for the UI
UI_GREETINGS = [
    "Welcome to your cozy news corner! 🏠",
    "Tom Nook's Daily News Emporium! 🦝",
    "Fresh news, delivered with island vibes! 🌴",
    "Your daily dose of world happenings! 🌍",
    "News as fresh as morning coffee! ☕"
]

@app.route("/")
def index():
    """Main news page"""
    db = SessionLocal()
    
    try:
        # Get recent articles by category
        ai_articles = db.execute(
            select(Article)
            .where(Article.category == "ai_frontier")
            .order_by(desc(Article.published))
            .limit(25)
        ).scalars().all()
        
        econ_articles = db.execute(
            select(Article)
            .where(Article.category == "economics_politics")
            .order_by(desc(Article.published))
            .limit(25)
        ).scalars().all()
        
        # Get some stats for fun
        total_articles = db.execute(select(func.count(Article.id))).scalar()
        
        # Get articles from today
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = db.execute(
            select(func.count(Article.id))
            .where(Article.published >= today)
        ).scalar()
        
    finally:
        db.close()
    
    return render_template(
        "index.html",
        ai_articles=ai_articles,
        econ_articles=econ_articles,
        greeting=random.choice(UI_GREETINGS),
        total_articles=total_articles,
        today_count=today_count,
        current_time=datetime.now().strftime("%B %d, %Y at %I:%M %p")
    )

@app.route("/refresh")
def refresh_feeds():
    """Manually refresh feeds"""
    try:
        new_articles = fetch_feeds()
        return jsonify({
            "success": True,
            "message": f"🎉 Successfully added {new_articles} new articles!",
            "new_count": new_articles
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"❌ Error refreshing feeds: {str(e)}"
        }), 500

@app.route("/send-digest")
def send_digest_now():
    """Manually send email digest"""
    try:
        success = send_digest()
        if success:
            return jsonify({
                "success": True,
                "message": "📧 Daily digest sent successfully! Check your email! ✉️"
            })
        else:
            return jsonify({
                "success": False,
                "message": "❌ Failed to send digest. Check email configuration."
            }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"❌ Error sending digest: {str(e)}"
        }), 500

@app.route("/stats")
def stats():
    """Get some fun statistics"""
    db = SessionLocal()
    
    try:
        # Basic stats
        total_articles = db.execute(select(func.count(Article.id))).scalar()
        
        # Articles by category
        ai_count = db.execute(
            select(func.count(Article.id))
            .where(Article.category == "ai_frontier")
        ).scalar()
        
        econ_count = db.execute(
            select(func.count(Article.id))
            .where(Article.category == "economics_politics")
        ).scalar()
        
        # Recent activity
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = db.execute(
            select(func.count(Article.id))
            .where(Article.published >= today)
        ).scalar()
        
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_count = db.execute(
            select(func.count(Article.id))
            .where(Article.published >= week_ago)
        ).scalar()
        
        # Top sources
        top_sources = db.execute(
            select(Article.source, func.count(Article.id).label('count'))
            .group_by(Article.source)
            .order_by(desc('count'))
            .limit(5)
        ).all()
        
    finally:
        db.close()
    
    return jsonify({
        "total_articles": total_articles,
        "ai_articles": ai_count,
        "econ_articles": econ_count,
        "today_articles": today_count,
        "week_articles": week_count,
        "top_sources": [{"name": source, "count": count} for source, count in top_sources]
    })

# Set up scheduled tasks
def setup_scheduler():
    """Set up background scheduler for daily tasks"""
    scheduler = BackgroundScheduler(daemon=True)
    
    # Daily news fetch at 6 AM
    scheduler.add_job(
        func=fetch_feeds,
        trigger="cron",
        hour=6,
        minute=0,
        id="daily_fetch"
    )
    
    # Daily email digest at 7 AM
    scheduler.add_job(
        func=send_digest,
        trigger="cron",
        hour=7,
        minute=0,
        id="daily_digest"
    )
    
    # Additional refresh at 6 PM for evening news
    scheduler.add_job(
        func=fetch_feeds,
        trigger="cron",
        hour=18,
        minute=0,
        id="evening_fetch"
    )
    
    scheduler.start()
    print("📅 Scheduled daily tasks activated! Like Isabelle's morning announcements! 📢")
    return scheduler

if __name__ == "__main__":
    # Initialize with some data on first run
    print("🌅 Starting Animal Crossing News! 🌟")
    
    # Set up scheduler
    scheduler = setup_scheduler()
    
    try:
        # Try to fetch some initial data
        print("🔄 Fetching initial news...")
        fetch_feeds()
    except Exception as e:
        print(f"⚠️  Initial fetch failed: {e}")
        print("📝 You can manually refresh feeds from the web interface!")
    
    print("🚀 Starting server on http://localhost:8000")
    print("🏠 Your cozy news website is ready to go!")
    
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=os.getenv("FLASK_DEBUG", "0") == "1"
    )
