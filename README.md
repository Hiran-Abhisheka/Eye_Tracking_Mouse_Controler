# Eye Tracking Mouse Control

This tool allows you to control your mouse cursor using eye movements. It uses your webcam to track your eye movements and translate them into mouse cursor movements. You can also click by blinking.

## Features

- Eye tracking for mouse cursor control
- Blink detection for mouse clicks
- Automatic calibration
- Visual feedback and debugging information

## For Users

### Installation

1. Download the installer (`Eye_Tracking_Mouse_Control_Setup.exe`).
2. Run the installer and follow the instructions.
3. The application will be installed on your system and shortcuts will be created on your desktop and in the Start menu.

## For Developers

### Requirements

- Python 3.6 or higher
- Webcam
- The following Python packages:
  - OpenCV (cv2)
  - MediaPipe
  - PyAutoGUI
  - NumPy
  - PyInstaller (for building the executable)
  - Pillow (for icon creation)

### Building from Source

1. Install the required packages:

```
pip install -r requirements.txt
pip install pyinstaller pillow
```

### Usage (Source Code)

1. Run the script:

```
python eye_tracker.py
```

### Building Executable

1. Generate the icon:

```
python create_icon.py
```

2. Build the executable:

```
build_exe.bat
```

3. (Optional) Create an installer using NSIS:
   - Install NSIS (Nullsoft Scriptable Install System)
   - Right-click on `installer.nsi` and select "Compile NSIS Script"
   - The installer will be generated as `Eye_Tracking_Mouse_Control_Setup.exe`

### Usage (Installed Application)

1. Launch "Eye Tracking Mouse Control" from your desktop or Start menu.

2. When the program starts, it will enter calibration mode. Look around your screen normally for a few seconds.
3. After calibration completes, the mouse cursor will follow your eye movements.
4. Blink deliberately to perform a mouse click.
5. Press 'r' to recalibrate if needed.
6. Press 'q' to quit the application.

## Tips for Better Performance

- Ensure good lighting conditions for better face detection
- Try to keep your head relatively stable
- Adjust the `BLINK_THRESHOLD` in the code if blink detection is too sensitive or not sensitive enough
- Adjust the `smoothing_factor` for smoother or more responsive cursor movement

## Troubleshooting

- If the cursor movement is too sensitive or not sensitive enough, try recalibrating with the 'r' key
- If the application fails to detect your face, try improving lighting conditions
- If clicks are triggered too easily, adjust the `BLINK_THRESHOLD` to a lower value

## License

This project is open source and available under the MIT License.
