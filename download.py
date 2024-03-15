import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

def main() -> None:
    path = os.path.expanduser('~/Downloads')
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print("Monitoring for PDFs in Downloads folder. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class PDFHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Path to the folder where you want to move your PDFs
        destination_folder = os.path.expanduser('~/PDF')
        # Ensure the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        # Path to the folder you want to monitor (e.g., your Downloads folder)
        downloads_folder = os.path.expanduser('~/Downloads')
        
        # Loop through all files in the Downloads folder
        for filename in os.listdir(downloads_folder):
            # Check if the file is a PDF
            if filename.endswith('.pdf'):
                # Construct the full file paths
                src_path = os.path.join(downloads_folder, filename)
                dst_path = os.path.join(destination_folder, filename)
                
                # Move the PDF file
                os.rename(src_path, dst_path)
                print(f"Moved: {filename}")

                # Open the PDF file with the default application
                self.open_pdf(dst_path)

    def open_pdf(self, file_path):
        # Open the PDF with the default application
        subprocess.run(["open", file_path], check=True)

if __name__ == "__main__":
    main()
