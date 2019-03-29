$Version = "release";
$Path = $env:TEMP; 
$Zip = "GraphViz.zip"; 
$InstallDir = $env:homedrive+"\GraphViz"; 
Remove-Item $InstallDir;
mkdir $InstallDir;
Invoke-WebRequest "https://graphviz.gitlab.io/_pages/Download/windows/graphviz-2.38.zip" -OutFile $Path\$Zip; 
expand-archive -path $Path\$Zip -destinationpath $InstallDir;
Get-ChildItem -Path $InstallDir\$Version | Move-Item -Destination $InstallDir;
Remove-Item $InstallDir\$Version;
Remove-Item $Path\$Zip;

