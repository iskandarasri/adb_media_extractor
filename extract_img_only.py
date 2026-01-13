import os
from ppadb.client import Client as AdbClient

# Define supported image file extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', ".heic", ".heif"]

def run_adb_shell(device, command):
    # Execute a shell command on the connected Android device using ADB
    result = device.shell(command)
    return result.strip()

def pull_regular_images(device, remote_dir):
    # List files in the remote directory
    file_list = run_adb_shell(device, f'ls "{remote_dir}"').split()
    
    for file_name in file_list:
        remote_path = os.path.join(remote_dir, file_name).replace("\\", "/")
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        
        if ext in IMAGE_EXTENSIONS:
            # Pull image files to Android_Pictures folder
            local_path = os.path.join("Android_Pictures", file_name).replace("\\", "/")
            try:
                device.pull(remote_path, local_path)
                print(f"Extracted picture: {file_name}")
            except Exception as e:
                print(f"Failed to extract picture {file_name}: {e}")

def pull_whatsapp_images(device, remote_dir):
    # List files in the remote directory
    file_list = run_adb_shell(device, f'ls "{remote_dir}"').split()
    
    for file_name in file_list:
        remote_path = os.path.join(remote_dir, file_name).replace("\\", "/")
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        
        if ext in IMAGE_EXTENSIONS:
            # Pull image files to Android_Pictures_Whatsapp folder
            local_path = os.path.join("Android_Pictures_Whatsapp", file_name).replace("\\", "/")
            try:
                device.pull(remote_path, local_path)
                print(f"Extracted picture from WhatsApp: {file_name}")
            except Exception as e:
                print(f"Failed to extract picture from WhatsApp {file_name}: {e}")

def get_folders(device, folder):
    dir = f"/storage/emulated/0/{folder}"
    
    # Check if the directory exists on the Android device
    result = run_adb_shell(device, f'ls "{dir}"')
    if "No such file or directory" in result:
        print(f"{folder} directory not found on the device.")
        return []
    
    # List directories
    result = run_adb_shell(device, f'find "{dir}" -mindepth 1 -maxdepth 1 -type d')
    folders = [folder.strip() for folder in result.splitlines()]
    folders.append(dir)
    return folders

def get_pictures_from_android():
    # Connect to ADB and get the device list
    client = AdbClient(host="127.0.0.1", port=5037)
    try:
        devices = client.devices()
    except:
        print("Adb connection error.")
        return

    if not devices:
        print("No Android device found.")
        return

    # Get the first connected device (you can modify this if you have multiple devices connected)
    device = devices[0]

    # Create folders to store pictures
    if not os.path.exists("Android_Pictures"):
        os.makedirs("Android_Pictures")
        print("Created Android_Pictures folder")
    
    if not os.path.exists("Android_Pictures_Whatsapp"):
        os.makedirs("Android_Pictures_Whatsapp")
        print("Created Android_Pictures_Whatsapp folder")

    # Get folders for regular images
    folders = get_folders(device, "DCIM")
    folders.extend(get_folders(device, "Download"))
    folders.extend(get_folders(device, "Pictures"))
    
    # Get WhatsApp image folders
    foldersWhatsapp = get_folders(device, "Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images")

    # Pull regular images from each subdirectory
    for folder in folders:
        print(f"\nScanning folder: {folder}")
        pull_regular_images(device, folder)
    
    # Pull WhatsApp images from each subdirectory
    for folder in foldersWhatsapp:
        print(f"\nScanning WhatsApp folder: {folder}")
        pull_whatsapp_images(device, folder)
    
    print("\nImage extraction completed successfully!")

if __name__ == "__main__":
    get_pictures_from_android()