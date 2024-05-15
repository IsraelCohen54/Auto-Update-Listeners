import requests
import subprocess  # For secure updates using Git
from datetime import datetime, timedelta  # For scheduling daily checks
import os
import shutil

# Replace with your actual GitHub repository URL
repo_url = "https://api.github.com/repos/IsraelCohen54/Auto-Update-Listeners"
repo_cloning_url = "https://github.com/IsraelCohen54/Auto-Update-Listeners.git"


# Cloned folder relative path
folder_to_delete = "./updated_project"

check1_wow = 505

# Update check interval (in days)
update_interval = 1


def check_for_update():
    # Check if it's time for an update (based on interval)
    if datetime.now() - timedelta(seconds=update_interval) >= datetime.utcnow():  ## todo check utc
        response = requests.get(repo_url + "/releases/latest")
        if response.status_code == 200:
            latest_version_tag_name = response.json()["tag_name"]
            with open("version.txt", "r+") as f:  # Open in read/write mode
                ver = f.read()
                try:
                    # Attempt to convert version number to float (handles decimals)
                    current_version = float(ver)
                    latest_version = float(latest_version_tag_name)
                except ValueError:
                    # Handle non-numeric version formats (e.g., pre-release labels)
                    # todo write to github maybe?
                    #  print(f"Warning: Version format not recognized. Current: {ver},
                    #  Latest: {latest_version_tag_name}")
                    return  # Exit function if versions can't be compared numerically

                if latest_version > current_version:
                    update_script()
                    f.seek(0)  # Move to the beginning of the file
                    f.write(latest_version_tag_name)  # Overwrite version with new tag
                    f.truncate()  # Remove extra characters

                    # Use os.path.exists() to check if the folder exists before attempting to delete it
                    if os.path.exists(folder_to_delete):
                        # Use shutil.rmtree() to delete the folder and all of its contents recursively
                        shutil.rmtree(folder_to_delete)
                        print(f"Folder '{folder_to_delete}' and its contents deleted successfully.")
                    else:
                        print(f"Folder '{folder_to_delete}' does not exist.")


# todo defend vs internet crushes
# todo delete clone folder at end
def update_script():
    # Clone the entire repository (including updates)
    subprocess.run(["git", "clone", "--depth=1", repo_cloning_url, "./updated_project"])  # Clone into a sub-folder

    # Replace existing files with updated versions
    shutil.copy2("./updated_project/the_functionality.py", ".")
    shutil.copy2("./updated_project/updater.py", ".")
    shutil.copy2("./updated_project/version.txt", ".")

    # Optional: Restart functionality (consider platform-specific approaches)
    # subprocess.run(["python", "the_functionality.py"])  # Example for restarting

    print("Successfully updated project from GitHub!")


if __name__ == "__main__":
    check_for_update()
