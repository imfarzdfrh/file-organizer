import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# --- CONFIGURATION (Constants remain unchanged) ---
destination_paths = {
    "Pictures": "C:/Users/Lenovo/Pictures",
    "Documents": "C:/Users/Lenovo/Documents",
    "Videos": "C:/Users/Lenovo/Videos",
    "Music": "C:/Users/Lenovo/Music",
    "Others": "C:/Users/Lenovo/Desktop/Other_Files"
}

file_types = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav"]
}

# --- SCRIPT LOGIC (Your main code logic is placed in a function) ---
def organize_folder(source_path):
    """Organizes files in the selected folder."""
    if not source_path:
        messagebox.showwarning("Warning", "Please select a folder first.")
        return

    try:
        files_to_move = os.listdir(source_path)
        print(f"Starting to organize {len(files_to_move)} files from: {source_path}")

        for file_name in files_to_move:
            file_path = os.path.join(source_path, file_name)

            if os.path.isfile(file_path):
                moved = False
                for category, extensions in file_types.items():
                    if file_name.lower().endswith(tuple(extensions)):
                        dest_folder = destination_paths[category]
                        if not os.path.exists(dest_folder):
                            os.makedirs(dest_folder)
                        
                        shutil.move(file_path, dest_folder)
                        print(f"✅ Moved '{file_name}' to '{category}' folder.")
                        moved = True
                        break
                
                if not moved:
                    dest_folder = destination_paths["Others"]
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    
                    shutil.move(file_path, dest_folder)
                    print(f"❔ Moved '{file_name}' to 'Others' folder.")
        
        messagebox.showinfo("Success", "🎉 Files organized successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# --- GUI (Graphical User Interface) ---

# Function to open the folder selection dialog
def select_folder():
    """Opens the folder selection dialog and displays the path in the label."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_path_var.set(folder_selected)

# Create the main window
root = tk.Tk()
root.title("File Organizer")
root.geometry("400x150")

# Variable to hold the selected folder path
source_path_var = tk.StringVar()

# Create widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True)

select_button = tk.Button(frame, text="1. Select Folder", command=select_folder)
select_button.pack(pady=5)

path_label = tk.Label(frame, textvariable=source_path_var, fg="blue", wraplength=380)
path_label.pack(pady=5)

organize_button = tk.Button(frame, text="2. Start Organizing", command=lambda: organize_folder(source_path_var.get()))
organize_button.pack(pady=10)

# Run the main application loop
root.mainloop()
