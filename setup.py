"""
Setup script for installing the File Merger application.
"""

import subprocess
import sys
import os
from pathlib import Path


def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    
    requirements = [
        'PyPDF2==3.0.1',
        'openpyxl==3.1.2',
        'Pillow==10.0.0'
    ]
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing {package}: {e}")
            return False
    
    print("\n✓ All packages installed successfully!")
    return True


def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)."""
    if os.name != 'nt':
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "File Merger.lnk")
        target = os.path.join(os.getcwd(), "main.py")
        wDir = os.getcwd()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = target
        shortcut.save()
        
        print("✓ Desktop shortcut created")
        
    except ImportError:
        print("⚠ Could not create desktop shortcut (winshell not available)")
    except Exception as e:
        print(f"⚠ Could not create desktop shortcut: {e}")


def main():
    """Main setup function."""
    print("="*60)
    print("           FILE MERGER - Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        print("✗ Setup failed")
        sys.exit(1)
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\n" + "="*60)
    print("           SETUP COMPLETED")
    print("="*60)
    print("\nYou can now run the application:")
    print("  GUI Mode:  python main.py")
    print("  CLI Mode:  python main.py --cli")
    print("  Help:      python main.py --help")
    
    input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
