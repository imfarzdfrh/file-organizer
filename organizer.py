import os
import shutil

# --- CONFIGURATION ---
source_path = "C:/Users/Lenovo/Downloads"

# Destination folders for different file types
destination_paths = {
    "Pictures": "C:/Users/Lenovo/Pictures",
    "Documents": "C:/Users/Lenovo/Documents",
    "Videos": "C:/Users/Lenovo/Videos",
    "Music": "C:/Users/Lenovo/Music",
    "Others": "C:/Users/Lenovo/Desktop/Other_Files"  # For files that don't fit other categories
}

# File extensions for each category
file_types = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav"]
}

# --- SCRIPT LOGIC ---

# Check if the source folder exists
if not os.path.exists(source_path):
    print(f"Error: Source folder not found: {source_path}")
else:
    # Get a list of all files in the source folder
    files_to_move = os.listdir(source_path)

    print(f"Starting to organize {len(files_to_move)} files from: {source_path}")

    # Loop through each file to move it
    for file_name in files_to_move:
        file_path = os.path.join(source_path, file_name)

        # Make sure we are only processing files, not folders
        if os.path.isfile(file_path):
            moved = False
            # Find the correct category for the file based on its extension
            for category, extensions in file_types.items():
                if file_name.lower().endswith(tuple(extensions)):
                    dest_folder = destination_paths[category]

                    # Create the destination folder if it doesn't exist
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                        print(f"Created folder: {dest_folder}")

                    # Move the file
                    shutil.move(file_path, dest_folder)
                    print(f"✅ Moved '{file_name}' to '{category}' folder.")
                    moved = True
                    break  # Move to the next file

            # If the file type doesn't match any category, move it to the "Others" folder
            if not moved:
                dest_folder = destination_paths["Others"]
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                    print(f"Created folder: {dest_folder}")

                shutil.move(file_path, dest_folder)
                print(f"❔ Moved '{file_name}' to 'Others' folder.")

    print("\n🎉 File organization complete!")
