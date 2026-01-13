import subprocess

def main_menu():
    while True:
        print("\n========== Images and Videos Puller ADB ==========")
        print("This script pulls all images and videos from a connected Android device using ADB.")
        print("Made with love by Iskandar :)")
        print("Notes: Common folders are DCIM, Download, Pictures, Movies.")
        print()
        print("1. Retrieve all images only (Common folders)")
        print("2. Retrieve all videos only (Common folders)")
        print("3. Retrieve all images and videos (Common folders)")
        print("4. Retrieve all images and videos from WhatsApp only")
        print("5. Retrieve all images and videos from entire phone")
        print("6. Install required dependencies")
        print("7. Authorize ADB connection on Android device")
        print("8. Exit")
        print()
        print("====================================================")
        print()

        input_choice = input("Enter your choice (1-8): ").strip()
        print()
        
        if input_choice == '1':
            subprocess.run(['python', 'extract_img_only.py'])
            input("\nPress Enter to return to main menu...")
        elif input_choice == '2':
            subprocess.run(['python', 'extract_vids_only.py'])
            input("\nPress Enter to return to main menu...")
        elif input_choice == '3':
            subprocess.run(['python', 'extract_all.py'])
            input("\nPress Enter to return to main menu...")
        elif input_choice == '4':
            subprocess.run(['python', 'extract_img_vids_whatsapps.py'])
            input("\nPress Enter to return to main menu...")
        elif input_choice == '5':
            subprocess.run(['python', 'extract_entire_phone.py'])
            input("\nPress Enter to return to main menu...")
        elif input_choice == '6':
            subprocess.run(['python', '-m', 'pip', 'install', 'pure-python-adb==0.3.0.dev0'])
            input("\nPress Enter to return to main menu...")
        elif input_choice == '7':
            print("Please connect your Android device and authorize ADB connection.")
            subprocess.run(['adb', 'devices'])
            input("\nPress Enter to return to main menu...")
        elif input_choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()