import os
from ppadb.client import Client as AdbClient

# Define supported image and video file extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', ".heic", ".heif"]
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.gif']

def run_adb_shell(device, command):
    # Execute a shell command on the connected Android device using ADB
    result = device.shell(command)
    return result.strip()

def find_all_media_files(device):
    """Find all media files on the Android device"""
    print("Searching for all media files on the device...")
    
    # Use find command to locate all image and video files
    find_command = 'find /storage/emulated/0 -type f \\( '
    
    # Add image extensions
    for i, ext in enumerate(IMAGE_EXTENSIONS):
        if i > 0:
            find_command += ' -o '
        find_command += f'-iname "*{ext}"'
    
    find_command += ' -o '
    
    # Add video extensions
    for i, ext in enumerate(VIDEO_EXTENSIONS):
        if i > 0:
            find_command += ' -o '
        find_command += f'-iname "*{ext}"'
    
    find_command += ' \\)'
    
    result = run_adb_shell(device, find_command)
    
    if result:
        return result.splitlines()
    else:
        return []

def extract_single_file(device, remote_path, file_name):
    """Extract a single file to appropriate folder"""
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()
    
    # Determine which folder to use based on file type
    if ext in IMAGE_EXTENSIONS:
        folder = "Android_Pictures"
    elif ext in VIDEO_EXTENSIONS:
        folder = "Android_Videos"
    else:
        return False  # Not a media file
    
    # Create local path
    local_path = os.path.join(folder, file_name).replace("\\", "/")
    
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Extract the file
    try:
        device.pull(remote_path, local_path)
        return True
    except Exception as e:
        print(f"Failed to extract {file_name}: {e}")
        return False

def extract_all_media_files(device, media_files):
    """Extract all found media files"""
    total_files = len(media_files)
    print(f"Found {total_files} media files to extract")
    
    extracted_count = 0
    failed_count = 0
    
    for i, remote_path in enumerate(media_files, 1):
        file_name = os.path.basename(remote_path)
        
        # Show progress
        print(f"[{i}/{total_files}] Extracting: {file_name}")
        
        # Extract the file
        if extract_single_file(device, remote_path, file_name):
            extracted_count += 1
        else:
            failed_count += 1
    
    return extracted_count, failed_count

def get_all_media_from_android():
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

    # Get the first connected device
    device = devices[0]
    
    print("Starting extraction from entire Android device...")
    print("=" * 50)
    
    # Create main folders
    if not os.path.exists("Android_Pictures"):
        os.makedirs("Android_Pictures")
        print("Created Android_Pictures folder")
    
    if not os.path.exists("Android_Videos"):
        os.makedirs("Android_Videos")
        print("Created Android_Videos folder")
    
    # Find all media files
    media_files = find_all_media_files(device)
    
    if not media_files:
        print("No media files found on the device.")
        return
    
    # Extract all files
    extracted, failed = extract_all_media_files(device, media_files)
    
    # Print summary
    print("\n" + "=" * 50)
    print("EXTRACTION SUMMARY")
    print("=" * 50)
    print(f"Total files found: {len(media_files)}")
    print(f"Successfully extracted: {extracted}")
    print(f"Failed to extract: {failed}")
    print("\nExtraction completed successfully!")

if __name__ == "__main__":
    get_all_media_from_android()