#!/usr/bin/env python3
"""
Jupiter Route Visualizer Launcher
"""

import subprocess
import sys
import os

def check_dependencies():
    try:
        import streamlit
        import requests
        import pandas
        import plotly
        import networkx
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies using: pip install -r requirements.txt")
        return False

def main():
    print("🪐 Jupiter Route Visualizer")
    print("=" * 40)
    
    if not os.path.exists("jupiter_route_visualizer.py"):
        print("❌ Error: jupiter_route_visualizer.py not found!")
        print("Please run this script from the project directory.")
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    print("🚀 Starting Jupiter Route Visualizer...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 40)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "jupiter_route_visualizer.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 