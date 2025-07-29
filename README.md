# 🗂️ File Organizer

**A lightweight, portable tool to automatically organize your files by type (photos, videos, documents, etc.)**  
Just give it a folder path and it will sort everything neatly into separate directories!

---

## ✨ Features

- Automatically moves files into folders based on file type
- Portable `.exe` version — no need to install Python
- Custom destination paths for each file type
- Optional config file for advanced setups
- Easy-to-use command-line interface

---

## 🚀 Quick Start

### 🖥️ Run the Portable `.exe` Version

1. Go to the [Releases](https://github.com/imfarzdfrh/file-organizer/releases) page.
2. Download the latest `FileOrganizer.exe`.
3. Open a terminal and run:

```bash
FileOrganizer.exe --src "C:\Downloads" --photos "D:\Photos" --videos "D:\Videos"

Or use a config file:

FileOrganizer.exe --config "C:\myconfig.json"

⚙️ Sample config.json

{
  "src": "C:\\Downloads",
  "photos": "D:\\Sorted\\Photos",
  "videos": "D:\\Sorted\\Videos",
  "music": "D:\\Sorted\\Music",
  "documents": "D:\\Sorted\\Documents",
  "archives": "D:\\Sorted\\Archives",
  "others": "D:\\Sorted\\Others"
}

🧪 Run from Source (Python)

If you have Python installed:

git clone https://github.com/imfarzdfrh/file-organizer.git
cd file-organizer
pip install -r requirements.txt
python main.py --src "C:\Downloads" --photos "D:\Photos"

🛠 Build the .exe File (for developers)

pip install pyinstaller
pyinstaller --onefile --name FileOrganizer main.py

The compiled .exe will be in the dist/ folder.
📌 Command-Line Arguments
Argument	Description
--src	Source directory (required)
--photos	Target path for image files
--videos	Target path for video files
--music	Target path for music/audio files
--documents	Target path for documents (PDF, DOCX...)
--archives	Target path for zip/rar/7z files
--others	Target path for all other files
--config	Path to a config.json file
🤝 Contributing

Pull requests and feedback are welcome!
Feel free to open an issue or fork the repo to submit improvements.
📄 License

This project is licensed under the MIT License.
