import os
import sys

def delete_files_with_hr_version(directory):
    for root, dirs, files in os.walk(directory):
        # Create a set of files in the current directory
        files_set = set(files)
        
        for file in files:
            # Check if there is a file that starts with "hr-" and followed by the current file name
            hr_version = f"hr-{file}"
            
            if hr_version in files_set:
                # Get the full path of the file to be deleted
                file_to_delete = os.path.join(root, file)
                print(f"Deleting: {file_to_delete}")
                os.remove(file_to_delete)  # Uncomment this line to actually delete the file

if __name__ == "__main__":
    # Ensure a directory path is provided as a command line argument
    if len(sys.argv) < 2:
        print("Usage: python delete_files_with_hr_version.py <directory_path>")
        sys.exit(1)

    # Get the directory path from the command line argument
    directory = sys.argv[1]

    # Process the directory and delete files as needed
    delete_files_with_hr_version(directory)
