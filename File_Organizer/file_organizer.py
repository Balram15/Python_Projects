import os
import shutil
import hashlib
import logging
import csv
import tkinter as tk
from tkinter import filedialog


# Set up logging configuration
logging.basicConfig(filename="file_organizer.log", level=logging.INFO, format="%(asctime)s - %(message)s")


# File categorization dictionary
folders = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'Videos': ['.mp4', '.avi', '.mkv'],
    'Music': ['.mp3', '.wav']
}

# Define extensions for temporary and unnecessary files
temp_extensions = ['.tmp', '.bak', '.log', '.swp']

# Function to log actions to CSV
def log_action_csv(action):
    with open('file_actions.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([action])  # Logging action in a row
    logging.info(action)

# Function to organize files based on extensions
def organize_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            file_extension = os.path.splitext(filename)[1].lower()

            for folder, extensions in folders.items():
                if file_extension in extensions:
                    folder_path = os.path.join(directory, folder)

                    # Create folder if it doesn't exist
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    # Move the file to the folder
                    shutil.move(filepath, os.path.join(folder_path, filename))
                    log_action(f"Moved {filename} to {folder}")
                    log_action_csv(f"Moved {filename} to {folder}")
                    print(f"Moved {filename} to {folder}")
                    break


# Function to detect duplicate files using hashing
def find_duplicates(directory):
    file_hashes = {}
    duplicates = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath):
            hash_value = hash_file(filepath)

            if hash_value in file_hashes:
                duplicates.append((filepath, file_hashes[hash_value]))
            else:
                file_hashes[hash_value] = filepath

    return duplicates


# Function to generate file hash
def hash_file(filepath, buffer_size=65536):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# Function to cleanup unnecessary files
def cleanup_unnecessary_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath) and any(filename.endswith(ext) for ext in temp_extensions):
            os.remove(filepath)
            log_action(f"Deleted unnecessary file: {filename}")
            log_action_csv(f"Deleted unnecessary file: {filename}")
            print(f"Deleted unnecessary file: {filename}")


# Function to log actions to console and CSV
def log_action(action):
    logging.info(action)
    print(action)


# GUI to select a folder
def select_folder():
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        print(f"Selected folder: {folder_path}")
        organize_files(folder_path)
        duplicates = find_duplicates(folder_path)
        for dup in duplicates:
            print(f"Duplicate found: {dup[0]} and {dup[1]}")
        cleanup_unnecessary_files(folder_path)


# Setting up the main Tkinter window
root = tk.Tk()
root.title("File Organizer and Cleanup Tool")

# Add a button to allow the user to select a folder
button = tk.Button(root, text="Select Folder to Organize and Clean", command=select_folder)
button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
