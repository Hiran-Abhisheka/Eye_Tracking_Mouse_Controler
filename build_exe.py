import os
import subprocess
import sys
import site
import shutil
import tempfile
from pathlib import Path

print("Building Eye Tracker Executable...")

# Check if PyInstaller is installed
try:
    import PyInstaller
    print("PyInstaller is installed.")
except ImportError:
    print("Installing PyInstaller...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])

# Check if icon exists
if not os.path.exists("icon.ico"):
    print("Creating icon...")
    subprocess.call([sys.executable, "create_icon.py"])

# Find MediaPipe resources
try:
    import mediapipe
    mediapipe_path = os.path.dirname(mediapipe.__file__)
    print(f"MediaPipe path: {mediapipe_path}")
except ImportError:
    print("MediaPipe not found. Please install it first.")
    sys.exit(1)

# Create a temporary spec file for PyInstaller
spec_content = """
# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

block_cipher = None

# Find MediaPipe data files
import mediapipe
mediapipe_path = Path(mediapipe.__file__).parent

# List all the MediaPipe resources to be included
mediapipe_data = [
    (str(mediapipe_path / 'modules'), 'mediapipe/modules'),
]

a = Analysis(
    ['eye_tracker.py'],
    pathex=[],
    binaries=[],
    datas=mediapipe_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Eye Tracking Mouse Control',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
"""

# Write the spec file
spec_path = "eye_tracker_fixed.spec"
with open(spec_path, "w") as f:
    f.write(spec_content)

print(f"Created spec file: {spec_path}")

# Build the executable using the spec file
print("Building executable with PyInstaller...")
cmd = [
    "pyinstaller",
    "--clean",
    spec_path
]

result = subprocess.call(cmd)

if result == 0:
    print("Build completed successfully!")
    print("The executable can be found in the 'dist' folder.")
else:
    print(f"Build failed with error code {result}")

input("Press Enter to continue...")
