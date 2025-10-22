#!/usr/bin/env python3
"""
Simple launcher for the enhanced drone GUI
"""

import subprocess
import sys
import os

def main():
    print("🚁 Enhanced Drone Simulator Launcher")
    print("=" * 40)
    
    # Check if the enhanced version exists
    if os.path.exists("enhanced_drone_gui.py"):
        print("✅ Enhanced drone GUI found")
        print("\n🚀 Launching Enhanced Drone Simulator...")
        print("\nNew Features:")
        print("- 🔍 Zoom and pan on both 3D view and graphs")
        print("- �� Hold buttons for continuous movement")
        print("- 🎨 Fresh, energetic modern interface")
        print("- 🔘 Modern button styling with emojis")
        print("- ⚡ Same smooth performance as original")
        print("\nControls:")
        print("- Hold any movement button for continuous action")
        print("- Use navigation toolbars to zoom graphs")
        print("- Red STOP button for emergency stop")
        
        try:
            subprocess.run([sys.executable, "enhanced_drone_gui.py"])
        except KeyboardInterrupt:
            print("\n\n✅ Simulator closed successfully.")
    else:
        print("❌ Enhanced drone GUI not found!")
        print("Make sure 'enhanced_drone_gui.py' is in the current directory.")

if __name__ == "__main__":
    main()
