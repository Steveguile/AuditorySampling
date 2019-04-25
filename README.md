# Welcome to the Auditory Sampler

This project was created as a final year project under the **Computing** course for **Bournemouth University**. The purpose of this project is to implement a system that accurately predicts the occurrence of road traffic incidents from auditory data.

It does this by **synthetically generating** data, performing **binary classification** on generated data, and displaying predictions on a lightweight **web application** . 

## Docker Setup for Windows:

Open Powershell

Set-ExecutionPolicy RemoteSigned
Run scripts\install_docker.ps1

**Installation of docker for this project currently only works for Windows, but the process for Linux can be found at: https://runnable.com/docker/install-docker-on-linux**

**Run:** 

docker build -t auditorysampler:v1.0 /path/to/directory **- create image from source**
docker run -it -p 8080:80 (external port : internal port) --name give_it_a_name auditorysampler:v1.0 **- create container from image**

docker ps -a **- check container exists with name give_it_a_name**

**Note**: Docker Desktop for Windows was used for its easy installation, and not having to set up Virtualbox. It is limited to 2GB memory under Hyper-V by default. If you would like to add more audio data that exceeds this memory limit (I.E process an audio file larger than 2GB), you can find examples on how to change this online.

**Note 2** You'll probably have to remove the Docker Desktop for Windows executable as the removal from the script fails because the exe is being used when it tries to delete it. 🤷

## In the container

These commands can be run in any order, but the full process uses commands 1, 2, 3, 4

| |Command                        					|Description                  |
|-|-------------------------------------------------|-----------------------------|
|1|python3 data_generator/SyntheticDataGenerator.py |Generate the audio files|
|2|python3 data_generator/AttributeGenerator.py		|Extract spectral features from files|
|3|python3 data_miner/Model.py						|Perform binary classification using best performing model|
|4|python3 web_application/Map.py					|Generate html file from predicted events|
|5|python3 data_miner/DataMiner.py					|Test classifiers for performance scores on data|


**To start the server -** service nginx start 

Connect to localhost port 8080 (or whichever you set as external port) on 

Recommended to run in Chrome, if installation does not currently exist, run scripts/install_chrome.ps1

## Don't Want to use Docker?
 
 <p>On windows, run initialize.py to install ffmpeg, graphiz, and chrome on your local machine. </p>
 
 Add this line: **;C:\GraphViz;C:\FFmpeg;**  to your system environment variable **Path** using the tutorial found at: https://support.microsoft.com/en-us/help/310519/how-to-manage-environment-variables-in-windows-xp

Now all files in this project should work :+1:

Order of file execution is the same as found above. Some other files exist that allow data preparation before image is created.

|File|Description|
|-|-|
|data_generator\AttributeGenerator.py</span>|Extract spectral features from files|
|data_generator\AudioCutter.py</span>|Shortens road traffic files to 30 minutes (so not too big for container)|
|data_generator\FormatConvert.py</span>|Converts file in directories to wav (not well configured at current version)|
|data_generator\SyntheticDataGenerator.py</span>|Generate the audio files|
|data_miner\DataMiner.py</span>|Test classifiers for performance scores on data, outputs classifiers at data\models\|
|data_miner\Model.py</span>|Perform binary classification using best performing model|
|data_miner\Plotter.py</span>|Plots heatmap and scatter plots for data, found at data\plots\|
|web_application\Map.py</span>|Generate html file from predicted events|

# Troubleshooting

Docker run / start gets port failure error like:

Error response from daemon: driver failed programming external connectivity on endpoint dazzling_payne (8438a2ea5c3964d0df7b61468e0b92a8d193b0d8743e1bb3f30b005d6e59f7fc): Error starting userland proxy: mkdir /port/tcp:0.0.0.0:8080:tcp:172.17.0.2:80: input/output error

Restart Docker Desktop for Windows

Basically any issue with Docker, just restart it.

