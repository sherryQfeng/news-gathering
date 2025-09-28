import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import random

try:
    from sqlalchemy import select, desc
    from models import SessionLocal, Article
except ImportError:
    print("Warning: SQLAlchemy not available. Install requirements first.")
    select = desc = SessionLocal = Article = None

# Fun greetings from our Animal Crossing friends
NEWSLETTER_GREETINGS = [
    "🌅 Good morning! Tom Nook here with your daily news roundup!",
    "🌟 Hello there! Isabelle has compiled today's most important updates!",
    "🦉 Greetings! Blathers found these fascinating articles for you!",
    "🎵 Hey hey! K.K. Slider picked out today's trending topics!",
    "⭐ Celeste spotted these stellar stories in today's news!"
]

NEWSLETTER_CLOSINGS = [
    "Stay curious and keep learning! 🌟 - Your Animal Crossing News Team",
    "Until tomorrow's news arrives! 🏠 - Tom Nook & Friends",
    "Remember to water your brain like you water your flowers! 🌸 - Isabelle",
    "Knowledge is the best investment! 💰 - Tom Nook",
    "Keep reaching for the stars! ⭐ - Celeste"
]

def build_digest_html():
    """Build HTML email digest of recent articles"""
    db = SessionLocal()
    
    try:
        # Get articles from the last 24 hours
        since = datetime.utcnow() - timedelta(days=1)
        
        # Fetch AI articles
        ai_articles = db.execute(
            select(Article)
            .where(Article.category == "ai_frontier", Article.published >= since)
            .order_by(desc(Article.published))
            .limit(15)
        ).scalars().all()
        
        # Fetch economics/politics articles
        econ_articles = db.execute(
            select(Article)
            .where(Article.category == "economics_politics", Article.published >= since)
            .order_by(desc(Article.published))
            .limit(15)
        ).scalars().all()
        
    finally:
        db.close()
    
    def build_section(title, articles, section_emoji):
        if not articles:
            return f"""
            <div style="margin: 20px 0;">
                <h3 style="color: #2F4F4F; font-family: 'Comic Sans MS', cursive; border-bottom: 2px solid #8FBC8F;">
                    {section_emoji} {title}
                </h3>
                <p style="font-style: italic; color: #666;">
                    🌙 All quiet on this front today! Check back tomorrow!
                </p>
            </div>
            """
        
        article_items = ""
        for article in articles:
            # Truncate long titles
            title = article.title if len(article.title) <= 80 else article.title[:77] + "..."
            
            article_items += f"""
            <div style="margin: 15px 0; padding: 15px; background: #F5F5DC; border-left: 4px solid #8FBC8F; border-radius: 5px;">
                <div style="margin-bottom: 8px;">
                    <span style="font-size: 18px;">{article.emoji}</span>
                    <strong><a href="{article.link}" style="color: #2F4F4F; text-decoration: none;">{title}</a></strong>
                </div>
                <div style="font-size: 12px; color: #666; margin-bottom: 8px;">
                    📡 {article.source} • 📅 {article.published.strftime('%B %d, %Y')}
                </div>
                {f'<div style="font-size: 14px; color: #444; margin-bottom: 8px; line-height: 1.4;">{article.summary}</div>' if article.summary else ''}
                <div style="font-style: italic; color: #8FBC8F; font-size: 13px; background: #E8F5E8; padding: 8px; border-radius: 3px;">
                    💭 {article.villager_comment}
                </div>
            </div>
            """
        
        return f"""
        <div style="margin: 20px 0;">
            <h3 style="color: #2F4F4F; font-family: 'Comic Sans MS', cursive; border-bottom: 2px solid #8FBC8F; padding-bottom: 5px;">
                {section_emoji} {title}
            </h3>
            {article_items}
        </div>
        """
    
    greeting = random.choice(NEWSLETTER_GREETINGS)
    closing = random.choice(NEWSLETTER_CLOSINGS)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Daily News Digest - Animal Crossing Style!</title>
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #2F4F4F; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #F0F8FF;">
        
        <!-- Header -->
        <div style="text-align: center; background: linear-gradient(135deg, #8FBC8F, #98FB98); padding: 20px; border-radius: 15px; margin-bottom: 30px;">
            <h1 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-family: 'Comic Sans MS', cursive; margin: 0;">
                🌟 Daily News Digest 🌟
            </h1>
            <p style="color: white; font-size: 16px; margin: 10px 0 0 0;">
                Animal Crossing Style • Your Daily Dose of World Happenings!
            </p>
        </div>
        
        <!-- Greeting -->
        <div style="background: #FFB6C1; padding: 15px; border-radius: 10px; margin-bottom: 25px; text-align: center;">
            <p style="margin: 0; font-size: 16px; font-weight: bold;">
                {greeting}
            </p>
        </div>
        
        <!-- Content Sections -->
        {build_section("AI Frontier & Technology", ai_articles, "🤖")}
        {build_section("Economics & Politics", econ_articles, "💰")}
        
        <!-- Footer -->
        <div style="background: #E8F5E8; padding: 20px; border-radius: 10px; text-align: center; margin-top: 30px;">
            <p style="margin: 0; font-size: 14px; color: #2F4F4F;">
                {closing}
            </p>
            <p style="margin: 10px 0 0 0; font-size: 12px; color: #666;">
                🏝️ Delivered with love from your digital island paradise! 🏝️
            </p>
        </div>
        
    </body>
    </html>
    """
    
    return html_content

def send_digest():
    """Send the daily news digest email"""
    print("📧 Preparing to send daily digest... (like sending a letter to a friend!) ✉️")
    
    # Get email configuration
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL", smtp_username)
    to_email = os.getenv("TO_EMAIL", smtp_username)
    
    if not all([smtp_host, smtp_username, smtp_password, to_email]):
        print("❌ Email configuration incomplete! Check your environment variables.")
        return False
    
    try:
        # Create email message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🌟 Daily News Digest - {datetime.now().strftime('%B %d, %Y')} 🌟"
        message["From"] = from_email
        message["To"] = to_email
        
        # Build HTML content
        html_content = build_digest_html()
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, [to_email], message.as_string())
        
        print("✅ Daily digest sent successfully! 🎉")
        print("📬 Your news should arrive shortly! (faster than Gulliver's mail!) ⛵")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send digest: {e}")
        return False

if __name__ == "__main__":
    send_digest()
