# Set-ExecutionPolicy RemoteSigned

# Enable Hyper-V
DISM /Online /Enable-Feature /All /FeatureName:Microsoft-Hyper-V

# Install Docker Desktop for Windows
$DownloadLink = "https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe"
$Path = $env:TEMP; 
$Exe = "Docker for Windows Installer.exe"; 
$InstallDir = $env:homedrive+"\Program Files\Docker"; 
Remove-Item $InstallDir
Invoke-WebRequest $DownloadLink -OutFile $Path\$Exe; 
& $Path\$Exe; 
Remove-Item $Path\$Exe; 