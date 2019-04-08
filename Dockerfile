# Get base image
FROM ubuntu:18.04

MAINTAINER stevewhitehead pal <stephenewhitehead@outlook.com>

# RUN gets executed when building image
RUN apt-get update

RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install ffmpeg
RUN apt-get -y install graphviz


# Requirement for pyodbc
RUN apt-get -y install unixodbc-dev

COPY . /src
WORKDIR /src

RUN pip3 install -r /src/dependencies.txt

# For some reason pip3 wont' install geopip unless already installed using pip 
RUN apt-get -y install python-pip 
RUN pip install geopip
RUN pip3 install geopip


# CMD gets executed upon creation of container

CMD ["echo", "Welcome to Auditory Sampler"]
CMD ["/bin/bash"]
 