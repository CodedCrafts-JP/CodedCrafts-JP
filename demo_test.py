#!/usr/bin/env python3
"""
Demo script to test the drone simulator functionality
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are available"""
    try:
        import tkinter
        import matplotlib
        import numpy
        print("✅ All dependencies are available")
        print(f"   - tkinter: Available")
        print(f"   - matplotlib: {matplotlib.__version__}")
        print(f"   - numpy: {numpy.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    print("🚁 Drone Simulator Demo Test")
    print("=" * 40)
    
    if not check_dependencies():
        print("\nPlease install missing dependencies:")
        print("pip install matplotlib numpy")
        return
    
    print("\nAvailable simulators:")
    print("1. Basic Enhanced Version (improved_drone_gui.py)")
    print("2. Advanced Full-Featured Version (advanced_drone_gui.py)")
    
    choice = input("\nSelect version to run (1 or 2): ").strip()
    
    if choice == "1":
        script = "improved_drone_gui.py"
    elif choice == "2":
        script = "advanced_drone_gui.py"
    else:
        print("Invalid choice. Running advanced version by default.")
        script = "advanced_drone_gui.py"
    
    if os.path.exists(script):
        print(f"\n🚀 Launching {script}...")
        print("\nControls:")
        print("- Use mouse buttons for drone movement")
        print("- Keyboard: WASD for movement, QE for up/down")
        print("- Space: Emergency stop, R: Reset position")
        print("- Use navigation toolbars to zoom graphs")
        print("\nEnjoy the exhibition-ready drone simulator!")
        
        try:
            subprocess.run([sys.executable, script])
        except KeyboardInterrupt:
            print("\n\nSimulator closed.")
    else:
        print(f"❌ Script {script} not found!")

if __name__ == "__main__":
    main()
