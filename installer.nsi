; Eye Tracking Mouse Control Installer Script

; Set the name of the installer
Name "Eye Tracking Mouse Control"
OutFile "Eye_Tracking_Mouse_Control_Setup.exe"
Unicode True

; Default installation directory
InstallDir "$PROGRAMFILES\Eye Tracking Mouse Control"

; Request application privileges
RequestExecutionLevel admin

;--------------------------------
; Pages

Page directory
Page instfiles

;--------------------------------
; Installation section

Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Add files to the installation directory
  File "dist\Eye Tracking Mouse Control.exe"
  File "icon.ico"
  
  ; Create data directory for MediaPipe resources
  CreateDirectory "$INSTDIR\mediapipe"
  CreateDirectory "$INSTDIR\mediapipe\modules"
  
  ; Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\Eye Tracking Mouse Control"
  CreateShortcut "$SMPROGRAMS\Eye Tracking Mouse Control\Eye Tracking Mouse Control.lnk" "$INSTDIR\Eye Tracking Mouse Control.exe" "" "$INSTDIR\icon.ico"
  CreateShortcut "$DESKTOP\Eye Tracking Mouse Control.lnk" "$INSTDIR\Eye Tracking Mouse Control.exe" "" "$INSTDIR\icon.ico"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Add uninstall information to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Eye Tracking Mouse Control" "DisplayName" "Eye Tracking Mouse Control"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Eye Tracking Mouse Control" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Eye Tracking Mouse Control" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Eye Tracking Mouse Control" "Publisher" "Eye Tracking Tools"
SectionEnd

;--------------------------------
; Uninstaller section

Section "Uninstall"
  ; Remove installed files
  Delete "$INSTDIR\Eye Tracking Mouse Control.exe"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\Uninstall.exe"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\Eye Tracking Mouse Control\Eye Tracking Mouse Control.lnk"
  Delete "$DESKTOP\Eye Tracking Mouse Control.lnk"
  RMDir "$SMPROGRAMS\Eye Tracking Mouse Control"
  
  ; Remove installation directory
  RMDir "$INSTDIR"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Eye Tracking Mouse Control"
SectionEnd
