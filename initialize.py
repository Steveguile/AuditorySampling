import subprocess

# Purpose of this file is to make sure dependencies of the project are installed before any scripts are run

def install_chrome():
    command_line = 'powershell -ExecutionPolicy ByPass -File scripts\install_chrome.ps1'
    subprocess.Popen(command_line, shell=True)


def main():
    install_chrome()


main()