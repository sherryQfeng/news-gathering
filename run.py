#!/usr/bin/env python3
"""
🌟 Animal Crossing News Hub - Quick Start Script 🌟

This script helps you get your whimsical news site up and running quickly!
Run this instead of app.py for a guided setup experience.
"""

import os
import sys
from dotenv import load_dotenv
from fetch import fetch_feeds
from models import init_db

def print_banner():
    """Print a fun welcome banner"""
    banner = """
    🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟
    
         🏠 Welcome to Animal Crossing News Hub! 🏠
    
    🦝 Tom Nook says: "Let's get your news site ready!"
    🐕 Isabelle adds: "This will only take a moment!"
    
    🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟
    """
    print(banner)

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking your environment setup...")
    
    load_dotenv()
    
    required_vars = {
        'SMTP_HOST': 'Email server host',
        'SMTP_USERNAME': 'Your email username',
        'SMTP_PASSWORD': 'Your email password/app key',
        'TO_EMAIL': 'Where to send your daily digest'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  • {var}: {description}")
    
    if missing_vars:
        print("⚠️  Missing email configuration! Please set up your .env file:")
        for var in missing_vars:
            print(var)
        print("\n📝 Copy .env.example to .env and fill in your email settings!")
        print("💡 For Gmail, you'll need an App Password (not your regular password)")
        return False
    
    print("✅ Environment looks good!")
    return True

def setup_database():
    """Initialize the database"""
    print("🗄️  Setting up your database...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def initial_feed_fetch():
    """Fetch initial news articles"""
    print("📡 Fetching your first batch of news articles...")
    print("   (This might take a minute while we gather news from around the world!)")
    
    try:
        new_articles = fetch_feeds()
        if new_articles > 0:
            print(f"🎉 Successfully gathered {new_articles} articles!")
            print("🌟 Your news hub is now ready with fresh content!")
        else:
            print("📰 No new articles found, but that's okay!")
            print("🔄 Articles will be fetched automatically twice daily!")
        return True
    except Exception as e:
        print(f"⚠️  Initial fetch had some issues: {e}")
        print("🤔 This might be due to network issues or RSS feeds being unavailable")
        print("✅ Don't worry - you can refresh feeds manually from the web interface!")
        return False

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting your Animal Crossing News Hub!")
    print("🌐 Your site will be available at: http://localhost:8000")
    print("📧 Daily emails are scheduled for 7 AM (if configured)")
    print("🔄 News updates happen automatically at 6 AM and 6 PM")
    print("\n🏠 Have fun staying informed with your cozy news corner! 🌟")
    print("\n" + "="*60)
    
    # Import and run the app
    from app import app, setup_scheduler
    
    # Setup scheduler
    setup_scheduler()
    
    # Run the app
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=os.getenv("FLASK_DEBUG", "0") == "1"
    )

def main():
    """Main setup and run function"""
    print_banner()
    
    # Check environment
    env_ok = check_environment()
    
    # Setup database
    if not setup_database():
        print("💥 Cannot continue without database setup!")
        sys.exit(1)
    
    # Fetch initial articles
    initial_feed_fetch()
    
    # Show email status
    if not env_ok:
        print("\n📧 Email features will be disabled until you configure your .env file")
        print("🌐 But your web interface will work perfectly!")
    
    print("\n🎮 Ready to start? Press Ctrl+C to stop the server when you're done!")
    input("Press Enter to launch your news hub... ")
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()
