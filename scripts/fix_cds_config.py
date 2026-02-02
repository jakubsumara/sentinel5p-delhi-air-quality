"""
Helper script to fix CDS API configuration.
Updates .cdsapirc file to use the new API format.
"""

import os
import sys

def fix_cds_config():
    """Fix CDS API configuration file."""
    print("="*60)
    print("CDS API Configuration Fix")
    print("="*60)
    print()
    
    # Determine config file location
    if sys.platform == 'win32':
        config_file = os.path.join(os.environ['USERPROFILE'], '.cdsapirc')
    else:
        config_file = os.path.join(os.path.expanduser('~'), '.cdsapirc')
    
    print(f"Config file location: {config_file}")
    print()
    
    # Check if file exists
    if os.path.exists(config_file):
        print("Current configuration:")
        with open(config_file, 'r') as f:
            content = f.read()
            print(content)
        print()
        
        # Check if it needs updating
        if '/api/v2' in content or ':YOUR_API_KEY' in content:
            print("[WARNING] Configuration needs updating!")
            print()
            print("The new format should be:")
            print("  url: https://cds.climate.copernicus.eu/api")
            print("  key: YOUR_API_KEY")
            print()
            print("Note: Remove the UID prefix from the key!")
            print()
            
            response = input("Do you want to update it automatically? (y/n): ").strip().lower()
            if response == 'y':
                # Read current config
                with open(config_file, 'r') as f:
                    lines = f.readlines()
                
                # Update lines
                new_lines = []
                for line in lines:
                    if line.startswith('url:'):
                        new_lines.append('url: https://cds.climate.copernicus.eu/api\n')
                    elif line.startswith('key:'):
                        # Remove UID prefix if present
                        key_part = line.split(':', 1)[1].strip()
                        if ':' in key_part:
                            # Has UID prefix, remove it
                            key_part = key_part.split(':', 1)[1]
                        new_lines.append(f'key: {key_part}\n')
                    else:
                        new_lines.append(line)
                
                # Write updated config
                with open(config_file, 'w') as f:
                    f.writelines(new_lines)
                
                print("[OK] Configuration updated!")
                print()
                print("New configuration:")
                with open(config_file, 'r') as f:
                    print(f.read())
            else:
                print("Please update manually.")
        else:
            print("[OK] Configuration looks correct!")
    else:
        print("[INFO] Configuration file not found.")
        print()
        print("Create it with the following content:")
        print()
        print("url: https://cds.climate.copernicus.eu/api")
        print("key: YOUR_API_KEY")
        print()
        print("To get your API key:")
        print("1. Go to: https://cds.climate.copernicus.eu/#!/home")
        print("2. Click 'Your profile' -> 'API key'")
        print("3. Copy your API key (NOT the UID:KEY format, just the key)")
        print()
        
        response = input("Do you want to create the file now? (y/n): ").strip().lower()
        if response == 'y':
            api_key = input("Enter your API key: ").strip()
            
            with open(config_file, 'w') as f:
                f.write('url: https://cds.climate.copernicus.eu/api\n')
                f.write(f'key: {api_key}\n')
            
            print(f"[OK] Configuration file created at: {config_file}")
        else:
            print("Please create the file manually.")
    
    print()
    print("Next steps:")
    print("1. Update cdsapi: pip install --upgrade cdsapi")
    print("2. Test: python scripts/download_era5.py")

if __name__ == "__main__":
    fix_cds_config()
