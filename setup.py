import sys
from cx_Freeze import setup, Executable

# Define the base options for the setup
options = {
    "build_exe": {
        "include_files": ["NpasInSvcByLocRpt.csv"],
        "packages": ["os", "sys"],  # Replace with your package name
        "includes": ["csv", "ctypes", "re", "pyperclip", "tkinter"],  # List any additional modules you want to include
    }
}

# List of executables
executables = [
    Executable(
        r"C:\Users\bryan\Documents\ReddSummitApps\NumberManipulator_GUI\NumberManipulatorGUI.py",  # Replace with the name of your main script
        base=None,  # Set this to None if you don't want a console window
        #targetName="NumberManipulator.exe",  # Name of the generated executable
    )
]

# Setup the project
setup(
    name="NumberManipulator",
    version="1.1",
    description="SDR Number Manipulator tool",
    options=options,
    executables=executables
)
