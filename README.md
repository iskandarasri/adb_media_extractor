# Images and Videos Puller ADB

A command-line tool and GUI that helps you transfer media files (images and videos) from an Android device to your computer using ADB (Android Debug Bridge). The program provides a simple menu interface to select which types of files to extract and from which locations on the device.

## Key Features

* Extract images or videos separately, or both together
* Target common folders (DCIM, Download, Pictures, Movies)
* Extract WhatsApp media specifically
* Option to search the entire phone for media files
* Includes ADB setup and dependency installation helpers
* User-friendly menu interface

## Getting Started

### Dependencies

* Make sure python and pip already installed on your machine.
* You can run the program and select "Install Dependencies".

### Installing

```
git clone https://github.com/iskandarasri/adb_media_extractor.git
cd adb_media_extractor
```

### Executing program

* To run this program in command line interface (CLI), run this command:
```
python main.py
```

* To run this program in graphical user inteface (GUI), run this command:
```
python gui_main.py
```

## Extracted media
Notes: "Common"  in this program means it will extract media from folders DCIM, Download, Pictures, Movies.
This folders will appears in the current directory where all your images and videos will be stored.

* Android_Pictures - Store images file type
* Android_Videos - Store videos file type
* Android_Pictures_Whatsapp - Store images retrieved from Whatsapp
* Android_Videos_Whatsapp - Store videos retrieved from Whatsapp

