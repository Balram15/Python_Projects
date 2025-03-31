# Smart File Organizer and Cleanup Tool

This Python-based tool helps you organize files in a specified directory by categorizing them based on their file extensions. It also helps identify and remove unnecessary or temporary files, and logs actions in both a `.log` file and a `.csv` file for future reference. 

The tool provides an easy-to-use GUI (Graphical User Interface) that lets you select a folder, organize its contents, find duplicates, and clean up unnecessary files with just a few clicks.

## Features

- **Organize Files:** Automatically categorizes files into folders based on file extensions (e.g., images, documents, videos, music).
- **Cleanup Unnecessary Files:** Deletes temporary and backup files (e.g., `.tmp`, `.bak`, `.log`).
- **Find Duplicates:** Detects and lists duplicate files based on their hash values.
- **CSV Logging:** Logs all actions (e.g., moved files, deleted files) in a CSV file for easy analysis.
- **Log File:** Logs actions with timestamps for future auditing and debugging.

## Requirements

- Python 3.x
- `shutil` (standard Python module, no need for installation)
- `hashlib` (standard Python module, no need for installation)
- `tkinter` (for GUI, comes with Python)
- `csv` (standard Python module, no need for installation)
- `logging` (standard Python module, no need for installation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/smart-file-organizer.git
