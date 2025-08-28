# Building Eye Tracking Mouse Control as an Executable

This document provides step-by-step instructions to convert the Python application into a standalone executable (.exe) file with an installer.

## Prerequisites

1. Make sure you have all the required packages installed:

```
pip install -r requirements.txt
pip install pyinstaller pillow
```

2. For creating an installer, you'll need to install NSIS (Nullsoft Scriptable Install System):
   - Download from https://nsis.sourceforge.io/Download
   - Install with default options

## Step 1: Generate the Icon

Run the following command to create the application icon:

```
python create_icon.py
```

## Step 2: Build the Executable

Run the build script to create the standalone executable:

```
build_exe.bat
```

This will:

- Package your Python application and all dependencies into a single .exe file
- Place the resulting file in the "dist" folder
- The executable will be named "Eye Tracking Mouse Control.exe"

## Step 3: Create the Installer

1. Right-click on the `installer.nsi` file
2. Select "Compile NSIS Script" from the context menu
   - If this option is not available, open NSIS and drag the .nsi file into it
3. Wait for the compilation to complete
4. The installer will be generated as `Eye_Tracking_Mouse_Control_Setup.exe` in the same folder

## Distribution

You can now distribute:

- The standalone executable from the "dist" folder
- The complete installer (`Eye_Tracking_Mouse_Control_Setup.exe`)

## Troubleshooting

- If PyInstaller reports missing dependencies, you may need to add them explicitly in the build_exe.bat file
- If the application doesn't work after installation, try running it as administrator
- For any webcam access issues, ensure the installed application has permission to access the camera
