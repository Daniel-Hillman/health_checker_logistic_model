#!/usr/bin/env python3
"""
🚀 Health Prediction Server Startup Script
Run this to start your awesome health prediction app!
"""

import subprocess
import sys
import os
import webbrowser
import time
from threading import Timer

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def open_browser():
    """Open browser after a delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5000')
    print("🌐 Opening browser...")

def main():
    print("🏥 R U Healthy & Co. - Health Prediction App")
    print("=" * 50)
    
    # Check if CSV file exists
    if not os.path.exists('synthetic_coffee_health_10000.csv'):
        print("❌ Error: synthetic_coffee_health_10000.csv not found!")
        print("Please make sure the CSV file is in the same directory.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start browser timer
    Timer(3.0, open_browser).start()
    
    print("🚀 Starting Flask server...")
    print("📱 Your app will open at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start Flask app
    try:
        from app import app, load_or_train_model
        if load_or_train_model():
            app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        else:
            print("❌ Failed to load/train model.")
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for using R U Healthy & Co.!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()