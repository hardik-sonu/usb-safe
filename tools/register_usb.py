import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.usb_identity import get_all_usb_drives

def main():
    print("USB Safe - Registration Tool\n")
    print("Scanning for connected USB storage devices...\n")
    
    drives = get_all_usb_drives()
    
    if not drives:
        print("No removable USB drives found.")
        return
        
    print(f"{'Drive':<10} | {'Label':<20} | {'Serial Number':<15} | {'File System':<10}")
    print("-" * 65)
    for d in drives:
        print(f"{d.drive_letter:<10} | {d.volume_label:<20} | {d.volume_serial:<15} | {d.file_system:<10}")
        
    print("\nTo authorize a device, add its Name and Serial Number to config/config.json")
    print("Example:")
    print('    {')
    print('        "name": "LAB-USB-01",')
    print('        "volume_serial": "XXXX-XXXX"')
    print('    }')

if __name__ == "__main__":
    main()
