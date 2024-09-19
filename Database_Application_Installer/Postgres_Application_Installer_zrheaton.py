import subprocess
import sys
import platform
import os
import logging
import shutil
import time

# Function to copy images to the current directory
def copy_images():
    src1 = 'C:/Users/zrhea/OneDrive/Desktop/Projects/PostgresApplication/Installer/Dependencies/logo1.png'
    src2 = 'C:/Users/zrhea/OneDrive/Desktop/Projects/PostgresApplication/Installer/Dependencies/logo2.png'

    dest = os.path.dirname(os.path.abspath(__file__))

    if os.path.abspath(src1) != os.path.join(dest, os.path.basename(src1)):
        shutil.copy(src1, dest)
        print(f"Copied {src1} to {dest}")
    else:
        print(f"Source and destination for {src1} are the same. Skipping copy.")

    if os.path.abspath(src2) != os.path.join(dest, os.path.basename(src2)):
        shutil.copy(src2, dest)
        print(f"Copied {src2} to {dest}")
    else:
        print(f"Source and destination for {src2} are the same. Skipping copy.")

# Configure logging
logging.basicConfig(filename='installer_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def install_package(package_name, command):
    logging.info(f"Attempting to install {package_name} using command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logging.info(f"{package_name} has been successfully installed.\nOutput: {result.stdout}\nError: {result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install {package_name}: {e}\nOutput: {e.stdout}\nError: {e.stderr}")
        return False
    return True

def check_and_install_packages(package_commands):
    missing_packages = []
    for package_name, commands in package_commands.items():
        try:
            __import__(package_name)
            logging.info(f"{package_name} is already installed.")
        except ImportError:
            installed = False
            for command in commands:
                if install_package(package_name, command):
                    try:
                        __import__(package_name)  # Recheck after installation
                        installed = True
                        break
                    except ImportError:
                        continue
            if not installed:
                missing_packages.append(package_name)

    if missing_packages:
        missing_str = ', '.join(missing_packages)
        logging.error(f"The following packages could not be installed automatically: {missing_str}\nPlease install them manually.")
        sys.exit(1)
    else:
        logging.info("All required packages are installed and ready to go!")

# Detect the operating system and set package installation commands
os_name = platform.system()
package_commands = {
    'PIL': ['pip install pillow' if os_name == 'Windows' else 'brew install pillow' if os_name == 'Darwin' else 'sudo apt-get install python3-pil'],
    'cowsay': ['pip install cowsay']
}

if os_name not in ["Windows", "Darwin", "Linux"]:
    logging.error(f"Unsupported OS: {os_name}")
    sys.exit(f"Unsupported OS: {os_name}")

# Checking and installing packages before starting the application
logging.info(f"Operating System: {os_name}")
logging.info(f"Python Executable: {sys.executable}")
logging.info(f"PATH Environment Variable: {os.environ['PATH']}")

# Verify pip is accessible
try:
    pip_check = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True, check=True)
    logging.info(f"pip is accessible: {pip_check.stdout}")
except subprocess.CalledProcessError as e:
    logging.error(f"pip check failed: {e}\nOutput: {e.stdout}\nError: {e.stderr}")
    sys.exit(1)

# Copy images
copy_images()

# Check and install packages
check_and_install_packages(package_commands)

# If all checks are passed, run the main installer script
installer_script_path = 'C:/Users/zrhea/OneDrive/Desktop/Projects/PostgresApplication/Installer/Dependencies/Installer_Part_5.py'
logging.info(f"Running {installer_script_path}")

try:
    subprocess.run([sys.executable, installer_script_path], check=True)
    logging.info(f"{installer_script_path} completed successfully")
except subprocess.CalledProcessError as e:
    logging.error(f"Failed to run {installer_script_path}: {e}")

input("Press Enter to continue...")

# Flush the logs
logging.shutdown()

