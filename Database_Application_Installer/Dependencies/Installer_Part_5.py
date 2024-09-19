import tkinter as tk
from tkinter import messagebox
import subprocess
import platform
import sys
from PIL import Image, ImageTk

def second_splash_screen():
    def start_installation():
        # Open a terminal and run the installwindowtest.py script
        if platform.system() == "Windows":
            subprocess.Popen(["start", "cmd", "/k", sys.executable, "C:/Users/zrhea/OneDrive/Desktop/Projects/PostgresApplication/Installer/Dependencies/installwindowtest.py"], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", "Terminal.app", sys.executable, "C:/Users/zrhea/OneDrive/Projects/PostgresApplication/Installer/Dependencies/installwindowtest.py"])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", sys.executable, "C:/Users/zrhea/OneDrive/Desktop/Projects/PostgresApplication/Installer/Dependencies/installwindowtest.py"])

    second_root = tk.Tk()
    if platform.system() == "Windows":
        second_root.state('zoomed')  # Maximize window on Windows
    else:
        second_root.attributes("-fullscreen", True)  # Fullscreen for MacOS/Linux
    second_root.title("Additional Installation Steps")

    # Create a main frame to hold the top label and bottom frames
    main_frame = tk.Frame(second_root, bg='purple')
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Add the top labels
    label = tk.Label(main_frame, text="Welcome to DataFusion", font=("Arial", 18), bg="purple", fg="white")
    label.pack(side=tk.TOP, fill=tk.X, pady=10)

    sub_label = tk.Label(main_frame, text="The System Has Been Checked For All The Required Tools", font=("Arial", 14), bg="purple", fg="white")
    sub_label.pack(side=tk.TOP, fill=tk.X)

    extra_label = tk.Label(main_frame, text="Click The Button Below To Continue When Ready", font=("Arial", 14), bg="purple", fg="white")
    extra_label.pack(side=tk.TOP, fill=tk.X)

    # Load and center the image (Update image path to include 'Dependencies' folder)
    image = Image.open("C:/Users/zrhea/OneDrive/Desktop/Projects/PostgresApplication/Installer/Dependencies/logo2.png")
    photo = ImageTk.PhotoImage(image)
    logo_label = tk.Label(main_frame, image=photo, bg='purple')
    logo_label.image = photo  # keep a reference!
    logo_label.pack(expand=True, pady=50)

    # Add a button to start the installation process below the image
    start_button = tk.Button(main_frame, text="Click here to start the installation process", command=start_installation, bg="white", fg="purple", font=("Arial", 14))
    start_button.pack(pady=20)

    second_root.mainloop()

def main_application():
    def exit_application():
        messagebox.showinfo("Exit", "Have a nice day!")
        root.destroy()

    def run_next_script():
        root.destroy()  # Close the main application window
        second_splash_screen()  # Open the second splash screen

    root = tk.Tk()
    if platform.system() == "Windows":
        root.state('zoomed')  # Maximize window on Windows
    else:
        root.attributes("-fullscreen", True)  # Fullscreen for MacOS/Linux
    root.title("DataFusion Installer")

    # Update the path for the first image to include 'Dependencies'
    image1 = Image.open("C:/Users/zrhea/OneDrive/Desktop/Projects/PostgresApplication/Installer/Dependencies/logo1.png")
    photo1 = ImageTk.PhotoImage(image1)

    logo_label = tk.Label(root, image=photo1, bg='purple')
    logo_label.image = photo1
    logo_label.pack(pady=20)

    welcome_label = tk.Label(root, text="Welcome to DataFusion", font=("Arial", 18), bg="purple", fg="white")
    welcome_label.pack(pady=30)

    next_button = tk.Button(root, text="Next", command=run_next_script, bg="white", fg="purple", width=20, height=2, font=("Arial", 18))
    next_button.pack(side=tk.RIGHT, padx=30, pady=40)

    exit_button = tk.Button(root, text="Exit", command=exit_application, bg="white", fg="purple", width=20, height=2, font=("Arial", 18))
    exit_button.pack(side=tk.LEFT, padx=30, pady=40)

    root.configure(background='purple')
    root.mainloop()

# Start the main application
main_application()
