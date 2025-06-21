#!/usr/bin/env python3
"""
Jupiter Portfolio Analyzer Launcher
===================================
Launches the Jupiter Portfolio Analyzer using Jupiter FREE APIs only.
No API key required - uses lite-api.jup.ag endpoints.
"""

import subprocess
import sys
import os
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def main():
    print("📊 Jupiter Portfolio Analyzer")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("✅ All dependencies are installed!")
    print("🚀 Starting Jupiter Portfolio Analyzer...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 40)
    
    # Launch the Jupiter Portfolio Analyzer
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "jupiter_portfolio_analyzer.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Jupiter Portfolio Analyzer stopped.")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main() 