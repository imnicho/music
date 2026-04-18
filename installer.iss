#define MyAppName "OctaveLights"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Nicho"
#define MyAppURL "https://github.com/nicho/octavelights"
#define MyAppExeName "OctaveLights.exe"
#define MyAppAssocName MyAppName + " Document"

[Setup]
AppId={{8B3D4C8E-7F9A-4B2C-8D5E-6A1F9C3E2B7D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
OutputDir=dist
OutputBaseFilename=OctaveLightsSetup
SetupIconFile=assets\app.ico
Compression=lz4
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Launch {#MyAppName} at Windows startup"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\OctaveLights\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\OctaveLights\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFileName: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFileName: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueName: "{#MyAppName}"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startup

[UninstallDelete]
Type: dirifempty; Name: "{app}"
Type: files; Name: "{userappdata}\OctaveLights\logs\*"
Type: dirifempty; Name: "{userappdata}\OctaveLights\logs"
Type: dirifempty; Name: "{userappdata}\OctaveLights"
