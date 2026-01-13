import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import threading
import subprocess
import queue
import os

# Import existing extraction modules
try:
    import extract_img_only
    import extract_vids_only
    import extract_all
    import extract_img_vids_whatsapps
    import extract_entire_phone
except ImportError as e:
    print(f"Error importing modules: {e}")

class RedirectText(object):
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag
        self.queue = queue.Queue()
        self.update_thread = threading.Thread(target=self.update_widget, daemon=True)
        self.update_thread.start()

    def write(self, string):
        self.queue.put(string)

    def flush(self):
        pass

    def update_widget(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            self.text_widget.configure(state='normal')
            self.text_widget.insert('end', text)
            self.text_widget.see('end')
            self.text_widget.configure(state='disabled')
            self.queue.task_done()

class MediaExtractorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Media Extractor ADB GUI by Iskandar")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, relief="flat", background="#007bff", foreground="white")
        self.style.map("TButton", background=[("active", "#0056b3")])

        self.create_widgets()
        self.redirect_logging()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg="#343a40", height=120)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="Images and Videos Puller ADB", font=("Segoe UI", 20, "bold"), bg="#343a40", fg="white")
        title_label.pack(pady=(20, 5))
        
        #subtitle_label = tk.Label(header_frame, text="Extract media from your Android device with ease", font=("Segoe UI", 10), bg="#343a40", fg="#adb5bd")
        subtitle_label = tk.Label(header_frame, text="Notes: \"Common\" will extract media from folders DCIM, Download, Pictures, Movies.", font=("Segoe UI", 10), bg="#343a40", fg="#adb5bd")
        subtitle_label.pack()

        # Main Content Area (Split into Controls and Log)
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Controls Frame (Left side)
        controls_frame = tk.LabelFrame(content_frame, text="Operations", bg="#f0f0f0", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        controls_frame.pack(side="left", fill="y", padx=(0, 20))

        # Buttons
        self.create_button(controls_frame, "Retrieve Images Only (Common)", self.run_extract_img_only)
        self.create_button(controls_frame, "Retrieve Videos Only (Common)", self.run_extract_vids_only)
        self.create_button(controls_frame, "Retrieve All Media (Common)", self.run_extract_all)
        self.create_button(controls_frame, "Retrieve WhatsApp Media Only", self.run_extract_whatsapp)
        self.create_button(controls_frame, "Retrieve Entire Phone Media", self.run_extract_entire_phone)
        
        separator = ttk.Separator(controls_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)

        self.create_button(controls_frame, "Install Dependencies", self.install_dependencies, color="#28a745")
        self.create_button(controls_frame, "Authorize ADB Connection", self.authorize_adb, color="#ffc107", text_color="black")
        self.create_button(controls_frame, "Exit", self.quit, color="#dc3545")

        # Log Frame (Right side)
        log_frame = tk.LabelFrame(content_frame, text="Log Output", bg="#f0f0f0", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        log_frame.pack(side="right", fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, state='disabled', font=("Consolas", 10), bg="#212529", fg="#f8f9fa", insertbackground="white")
        self.log_text.pack(fill="both", expand=True)

    def create_button(self, parent, text, command, color="#007bff", text_color="white"):
        btn = tk.Button(parent, text=text, command=lambda: self.run_in_thread(command, text), 
                        bg=color, fg=text_color, font=("Segoe UI", 10), relief="flat", cursor="hand2",
                        activebackground=self.adjust_color_brightness(color, -20), activeforeground=text_color,
                        width=35, pady=5, anchor="w", padx=10)
        btn.pack(pady=5, fill="x")
        return btn

    def adjust_color_brightness(self, hex_color, factor):
        # Helper to darken a hex color for active state
        # Very basic implementation, fallback to original if it fails
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            r = max(0, min(255, r + factor))
            g = max(0, min(255, g + factor))
            b = max(0, min(255, b + factor))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color

    def redirect_logging(self):
        sys.stdout = RedirectText(self.log_text)
        sys.stderr = RedirectText(self.log_text, tag="stderr")

    def run_in_thread(self, target_func, task_name):
        # Run the task in a separate thread so GUI doesn't freeze
        print(f"\n--- Starting: {task_name} ---")
        t = threading.Thread(target=self.wrapper_func, args=(target_func,))
        t.start()
        
    def wrapper_func(self, target_func):
        try:
            target_func()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("--- Task Completed ---")

    # Wrapper methods for existing scripts
    def run_extract_img_only(self):
        if 'extract_img_only' in sys.modules:
            extract_img_only.get_pictures_from_android()
        else:
            print("Error: extract_img_only module not loaded.")

    def run_extract_vids_only(self):
        if 'extract_vids_only' in sys.modules:
            extract_vids_only.get_videos_from_android()
        else:
            print("Error: extract_vids_only module not loaded.") # Note: function name in file was get_videos_from_android

    def run_extract_all(self):
        if 'extract_all' in sys.modules:
            extract_all.get_pictures_and_videos_from_android()
        else:
            print("Error: extract_all module not loaded.")

    def run_extract_whatsapp(self):
        if 'extract_img_vids_whatsapps' in sys.modules:
            extract_img_vids_whatsapps.get_pictures_from_android()
        else:
            print("Error: extract_img_vids_whatsapps module not loaded.")

    def run_extract_entire_phone(self):
        if 'extract_entire_phone' in sys.modules:
            extract_entire_phone.get_all_media_from_android()
        else:
            print("Error: extract_entire_phone module not loaded.")

    def install_dependencies(self):
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pure-python-adb==0.3.0.dev0'])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")

    def authorize_adb(self):
        print("Please connect your Android device")
        print("Checking ADB devices...")
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            print(result.stdout)
            print("If your device is listed as 'unauthorized', please check your phone screen.")
        except FileNotFoundError:
             # Try local adb.exe if system adb not found
             # Try local adb.exe if system adb not found
             adb_path = os.path.join(os.getcwd(), 'platform-tools', 'adb.exe')
             if os.path.exists(adb_path):
                  result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
                  print(result.stdout)
             else:
                print("ADB executable not found. Make sure adb.exe is in this folder or in your PATH.")

if __name__ == "__main__":
    app = MediaExtractorApp()
    app.mainloop()
