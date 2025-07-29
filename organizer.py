import os
import sys
import shutil
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

# --- HELPERS ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- SETTINGS ---
SETTINGS_FILE = "settings.json"

def load_settings():
    """Loads destination paths from the settings file."""
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default paths if file doesn't exist or is empty/corrupt
        return {
            "Pictures": "C:/Users/Lenovo/Pictures",
            "Documents": "C:/Users/Lenovo/Documents",
            "Videos": "C:/Users/Lenovo/Videos",
            "Music": "C:/Users/Lenovo/Music",
            "Others": "C:/Users/Lenovo/Desktop/Other_Files"
        }

def save_settings(paths):
    """Saves destination paths to the settings file."""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(paths, f, indent=2)

# --- CONFIGURATION ---
file_types = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav"]
}

# --- SCRIPT LOGIC ---
def organize_folder(source_path):
    """Organizes files in the selected folder based on current settings."""
    if not source_path:
        messagebox.showwarning("Warning", "Please select a folder first.")
        return

    current_paths = load_settings()

    try:
        files_to_move = os.listdir(source_path)
        if not files_to_move:
            messagebox.showinfo("Info", "The selected folder is empty.")
            return
            
        print(f"Starting to organize {len(files_to_move)} files from: {source_path}")

        moved_count = 0
        for file_name in files_to_move:
            file_path = os.path.join(source_path, file_name)

            if os.path.isfile(file_path):
                moved = False
                for category, extensions in file_types.items():
                    if file_name.lower().endswith(tuple(extensions)):
                        dest_folder = current_paths.get(category, current_paths["Others"])
                        if not os.path.exists(dest_folder):
                            os.makedirs(dest_folder)
                        
                        shutil.move(file_path, dest_folder)
                        print(f"✅ Moved '{file_name}' to '{category}' folder.")
                        moved = True
                        moved_count += 1
                        break
                
                if not moved:
                    dest_folder = current_paths["Others"]
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    
                    shutil.move(file_path, dest_folder)
                    print(f"❔ Moved '{file_name}' to 'Others' folder.")
                    moved_count += 1
        
        messagebox.showinfo("Success", f"🎉 {moved_count} files organized successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# --- GUI (Graphical User Interface) ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("File Organizer")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # --- Banner Image ---
        try:
            image_path = resource_path("assets/images/file.png")
            original_image = Image.open(image_path)
            original_width, original_height = original_image.size
            
            # Calculate new size while maintaining aspect ratio
            display_height = 50
            display_width = int(display_height * (original_width / original_height))
            
            self.banner_image = ctk.CTkImage(original_image, size=(display_width, display_height))
            self.banner_label = ctk.CTkLabel(self, text="", image=self.banner_image)
            self.banner_label.pack(pady=(10, 0))
            
            # Adjust window geometry dynamically
            window_height = display_height + 200 # image height + controls height
            self.geometry(f"500x{window_height}")

        except Exception as e:
            print(f"Error loading banner image: {e}")
            self.geometry("500x220") # Fallback geometry


        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Widgets ---
        self.select_button = ctk.CTkButton(self.main_frame, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=(15, 10))

        self.path_label = ctk.CTkLabel(self.main_frame, text="No folder selected", text_color="gray")
        self.path_label.pack(pady=5)

        self.organize_button = ctk.CTkButton(self.main_frame, text="Start Organizing", command=self.start_organizing, state="disabled")
        self.organize_button.pack(pady=10, padx=20, fill="x")


        # --- Settings Icon Button ---
        try:
            settings_icon_path = resource_path("assets/images/setting.png")
            settings_image = ctk.CTkImage(Image.open(settings_icon_path), size=(24, 24))
            self.settings_button = ctk.CTkButton(
                self, 
                text="", 
                image=settings_image, 
                command=self.open_settings_window,
                width=40,
                height=40,
                fg_color="transparent",
                hover_color="#333"
            )
            self.settings_button.place(relx=0.98, rely=0.98, anchor="se")
        except Exception as e:
            print(f"Error loading settings icon: {e}")
            # Fallback to a text button if icon fails
            self.settings_button = ctk.CTkButton(self.main_frame, text="Settings", command=self.open_settings_window)
            self.settings_button.pack(pady=(0, 20))


        self.source_path = ""
        self.settings_window = None

    def select_folder(self):
        """Opens the folder selection dialog and updates the UI."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_path = folder_selected
            self.path_label.configure(text=os.path.basename(folder_selected), text_color="white")
            self.organize_button.configure(state="normal")

    def start_organizing(self):
        organize_folder(self.source_path)

    def open_settings_window(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
            self.settings_window.grab_set() # Modal window
        else:
            self.settings_window.focus()


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Settings")
        self.geometry("600x300")
        self.transient(master)

        self.destination_paths = load_settings()
        self.path_vars = {category: ctk.StringVar(value=path) for category, path in self.destination_paths.items()}

        ctk.CTkLabel(self, text="Destination Folders", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        for category, path_var in self.path_vars.items():
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(fill='x', padx=20, pady=5)
            
            label = ctk.CTkLabel(frame, text=f"{category}:", width=10, anchor='w')
            label.pack(side='left', padx=(0, 10))
            
            entry = ctk.CTkEntry(frame, textvariable=path_var, width=350)
            entry.pack(side='left', expand=True, fill='x')
            
            browse_button = ctk.CTkButton(frame, text="...", width=30, command=lambda c=category: self.select_path(c))
            browse_button.pack(side='right', padx=(5, 0))

        apply_button = ctk.CTkButton(self, text="Apply & Close", command=self.apply_settings)
        apply_button.pack(pady=20)

    def select_path(self, category):
        """Opens a dialog to select a new path for a category."""
        new_path = filedialog.askdirectory()
        if new_path:
            self.path_vars[category].set(new_path)

    def apply_settings(self):
        """Saves the new paths and closes the settings window."""
        for category, path_var in self.path_vars.items():
            self.destination_paths[category] = path_var.get()
        save_settings(self.destination_paths)
        messagebox.showinfo("Success", "Settings saved successfully!", parent=self)
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
