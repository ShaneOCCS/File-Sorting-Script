import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Path to monitor for new downloads
DOWNLOADS_PATH = r"C:\Users\Shane\Downloads"

#File extensions mapped to their corresponding categories
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Archives": [".zip"],
    "Personal-Coding-Projects": [".py", ".java", ".js", ".html", ".css", ".c"]
}

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Handle file creation events in the downloads directory
        """
        #Skip if a directory was created
        if event.is_directory:
            return

        #Get the file extension
        _, ext = os.path.splitext(event.src_path)

        #Check each category to find a matching extension
        for folder, exts in CATEGORIES.items():
            if ext.lower() in exts:
                #Create a category subfolder if it doesn't exist
                dest_dir = os.path.join(DOWNLOADS_PATH, folder)
                os.makedirs(dest_dir, exist_ok=True)

                try:
                    #Move a file to the appropriate category folder
                    shutil.move(event.src_path, dest_dir)
                    print(f"Moved {os.path.basename(event.src_path)} → {folder}/")
                except Exception as e:
                    print(f"Error moving {os.path.basename(event.src_path)}")
                    print(e)
                break

#Watch the downloads directory for new files
if __name__ == "__main__":
    handler = DownloadHandler()
    observer = Observer()
    observer.schedule(handler, DOWNLOADS_PATH, recursive=False)
    observer.start()
    #Let the user know the watcher is running
    print(f"Watching {DOWNLOADS_PATH}…  (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
