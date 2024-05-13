import requests
import subprocess  # For secure updates using Git
from datetime import datetime, timedelta  # For scheduling daily checks

# Replace with your actual GitHub repository URL
repo_url = "https://api.github.com/repos/IsraelCohen54/Auto-Update-Listeners"


check1_wow = 505

# Update check interval (in days)
update_interval = 1


def check_for_update():
    # Check if it's time for an update (based on interval)
    if datetime.now() - timedelta(days=update_interval) >= datetime.utcnow():
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


def update_script():
    # Clone the entire repository (including updates)
    subprocess.run(["git", "clone", "--depth=1", repo_url, "./updated_project"])  # Clone into a sub-folder

    # Replace existing files with updated versions
    subprocess.run(["cp", "-r", "./updated_project/the_functionality.py", "."])
    subprocess.run(["cp", "-r", "./updated_project/updater.py", "."])
    subprocess.run(["cp", "-r", "./updated_project/version.txt", "."])

    # Optional: Restart functionality (consider platform-specific approaches)
    # subprocess.run(["python", "the_functionality.py"])  # Example for restarting

    print("Successfully updated project from GitHub!")


if __name__ == "__main__":
    check_for_update()
