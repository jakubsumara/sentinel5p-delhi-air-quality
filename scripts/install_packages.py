"""
Installation script for Sentinel-5P project dependencies.
This script installs all required packages from requirements.txt
"""

import subprocess
import sys
import os

# Fix Windows encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Installing: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("[OK] Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error occurred:")
        print(e.stderr)
        return False

def main():
    """Main installation function."""
    print("="*60)
    print("Sentinel-5P Project - Package Installation")
    print("="*60)
    print("\nThis script will install all required packages.")
    print("This may take several minutes...")
    
    # Check if requirements.txt exists
    requirements_file = os.path.join('..', 'requirements.txt')
    if not os.path.exists(requirements_file):
        requirements_file = 'requirements.txt'
    
    if not os.path.exists(requirements_file):
        print(f"\n[ERROR] Error: requirements.txt not found!")
        print("Make sure you're running this from the scripts/ directory")
        return False
    
    # Upgrade pip first
    print("\n" + "="*60)
    print("Step 1: Upgrading pip")
    print("="*60)
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    # Install packages from requirements.txt
    print("\n" + "="*60)
    print("Step 2: Installing packages from requirements.txt")
    print("="*60)
    success = run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        "All packages from requirements.txt"
    )
    
    if success:
        print("\n" + "="*60)
        print("[OK] Installation completed successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Run: python scripts/setup_check.py")
        print("2. Or open: notebooks/00_setup_verification.ipynb")
        print("\nFor Google Earth Engine:")
        print("  python -c 'import ee; ee.Authenticate()'")
    else:
        print("\n" + "="*60)
        print("[ERROR] Some packages failed to install")
        print("="*60)
        print("\nTroubleshooting:")
        print("1. Make sure you have internet connection")
        print("2. Try installing packages individually")
        print("3. Some packages may need system libraries:")
        print("   - Cartopy: may need PROJ and GEOS")
        print("   - On Windows: may need Visual C++ Build Tools")
        print("\nYou can try installing manually:")
        print(f"  {sys.executable} -m pip install -r {requirements_file}")
    
    return success

if __name__ == "__main__":
    main()
