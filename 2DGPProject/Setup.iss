; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A3680FB3-C586-4469-A528-E3C1F54DEA6F}
AppName=2DGPProject
AppVersion=1.0
;AppVerName=2DGPProject 1.0
AppPublisher=Chul
DefaultDirName={pf}\2DGPProject
DefaultGroupName=2DGPProject
OutputDir=\\Mac\Home\Repositories\2DGP_Project
OutputBaseFilename=2DGPProject
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "\\Mac\Home\Repositories\2DGP_Project\2DGPProject\dist\MyGame.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "\\Mac\Home\Repositories\2DGP_Project\2DGPProject\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\2DGPProject"; Filename: "{app}\MyGame.exe"
Name: "{commondesktop}\2DGPProject"; Filename: "{app}\MyGame.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MyGame.exe"; Description: "{cm:LaunchProgram,2DGPProject}"; Flags: nowait postinstall skipifsilent

