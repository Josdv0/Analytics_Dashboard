#!/usr/bin/env python
"""
Analytics Application Launcher
================================

Convenience script to launch the Analytics Dashboard with Streamlit.
Run this script instead of Analytics.py directly.

Usage:
    python run_analytics.py
"""

import subprocess
import sys
import os


def main():
    """Launch the Analytics Dashboard with Streamlit."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analytics_file = os.path.join(script_dir, "Analytics.py")
    
    # Build the streamlit command
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        analytics_file,
        "--logger.level=warning",  # Suppress debug warnings
        "--client.showErrorDetails=true",
        "--theme.base=dark"
    ]
    
    print("🚀 Starting Analytics Dashboard...")
    print(f"📊 Application: {analytics_file}")
    print("🌐 Open your browser at: http://localhost:8501")
    print("-" * 60)
    
    # Execute streamlit
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Analytics Dashboard stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
