import tkinter as tk
from gui import EncryptionApp
import os
import sys

def main():
    # Ensure the working directory is the same as the executable/script
    if getattr(sys, 'frozen', False):
        # If running as an EXE
        application_path = os.path.dirname(sys.executable)
    else:
        # If running as a script
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(application_path)

    # Create necessary directories if they don't exist
    for folder in ["encrypted_files", "decrypted_files"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
