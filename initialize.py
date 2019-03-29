import subprocess

# Purpose of this file is to make sure external dependencies of the project are installed before any scripts are run

def install_chrome():
    command_line = 'powershell -ExecutionPolicy ByPass -File scripts\install_chrome.ps1'
    subprocess.Popen(command_line, shell=True)


def install_ffmpeg():
    command_line = 'powershell -ExecutionPolicy ByPass -File scripts\install_ffmpeg.ps1'
    subprocess.Popen(command_line, shell=True)


def install_graphviz():
    command_line = 'powershell -ExecutionPolicy ByPass -File scripts\install_graphviz.ps1'
    subprocess.Popen(command_line, shell=True)


def main():
    install_chrome()
    install_ffmpeg()
    install_graphviz()

main()
