import os
import sys

def rename_hr_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file name starts with "hr-"
            if file.startswith("hr-"):
                # Remove "hr-" from the start of the file name
                new_file_name = file[3:]
                
                # Get the full paths of the old and new file names
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_file_name)
                
                # Rename the file
                print(f"Renaming: {old_file_path} to {new_file_path}")
                os.rename(old_file_path, new_file_path)  # Uncomment to perform the actual rename

if __name__ == "__main__":
    # Ensure a directory path is provided as a command line argument
    if len(sys.argv) < 2:
        print("Usage: python rename_hr_files.py <directory_path>")
        sys.exit(1)

    # Get the directory path from the command line argument
    directory = sys.argv[1]

    # Process the directory and rename files as needed
    rename_hr_files(directory)
