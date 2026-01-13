import os
from ppadb.client import Client as AdbClient

# Define supported image and video file extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', ".heic", ".heif"]
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.gif']

def run_adb_shell(device, command):
    # Execute a shell command on the connected Android device using ADB
    result = device.shell(command)
    return result.strip()

def pull_regular_files(device, remote_dir):
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
                
        elif ext in VIDEO_EXTENSIONS:
            # Pull video files to Android_Videos folder
            local_path = os.path.join("Android_Videos", file_name).replace("\\", "/")
            try:
                device.pull(remote_path, local_path)
                print(f"Extracted video: {file_name}")
            except Exception as e:
                print(f"Failed to extract video {file_name}: {e}")

def pull_whatsapp_files(device, remote_dir):
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
                
        elif ext in VIDEO_EXTENSIONS:
            # Pull video files to Android_Videos_Whatsapp folder
            local_path = os.path.join("Android_Videos_Whatsapp", file_name).replace("\\", "/")
            try:
                device.pull(remote_path, local_path)
                print(f"Extracted video from WhatsApp: {file_name}")
            except Exception as e:
                print(f"Failed to extract video from WhatsApp {file_name}: {e}")

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

def get_pictures_and_videos_from_android():
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

    # Create folders to store pictures and videos
    if not os.path.exists("Android_Pictures"):
        os.makedirs("Android_Pictures")
        print("Created Android_Pictures folder")
    
    if not os.path.exists("Android_Videos"):
        os.makedirs("Android_Videos")
        print("Created Android_Videos folder")
        
    if not os.path.exists("Android_Pictures_Whatsapp"):
        os.makedirs("Android_Pictures_Whatsapp")
        print("Created Android_Pictures_Whatsapp folder")       
        
    if not os.path.exists("Android_Videos_Whatsapp"):
        os.makedirs("Android_Videos_Whatsapp")
        print("Created Android_Videos_Whatsapp folder")

    # Get the list of subdirectories for regular folders
    folders = get_folders(device, "DCIM")
    folders.extend(get_folders(device, "Download"))
    folders.extend(get_folders(device, "Pictures"))
    folders.extend(get_folders(device, "Movies"))
    
    # Get WhatsApp folders
    foldersWhatsappImage = get_folders(device, "Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images")
    foldersWhatsappVideo = get_folders(device, "Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Video")

    # Pull regular pictures and videos from each subdirectory
    for folder in folders:
        print(f"\nScanning folder: {folder}")
        pull_regular_files(device, folder)
    
    # Pull WhatsApp pictures and videos from each subdirectory
    for folder in foldersWhatsappImage:
        print(f"\nScanning WhatsApp Image folder: {folder}")
        pull_whatsapp_files(device, folder) 
        
    for folder in foldersWhatsappVideo:
        print(f"\nScanning WhatsApp Video folder: {folder}")
        pull_whatsapp_files(device, folder)
    
    print("\nExtraction completed successfully!")

if __name__ == "__main__":
    get_pictures_and_videos_from_android()