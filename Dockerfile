# Get base image
FROM ubuntu:17.10


MAINTAINER stevewhitehead pal <stephenewhitehead@outlook.com>


# RUN gets executed when building image
RUN apt-get update


RUN apt-get -y install python3.6
RUN apt-get -y install python3-pip
RUN apt-get -y install ffmpeg
RUN apt-get -y install graphviz
RUN apt-get -y install chromium-browser


# Requirement for pyodbc
RUN apt-get -y install unixodbc-dev


COPY . /src/
RUN pip3 install -r /src/dependencies.txt


# For some reason pip3 wont install geopip unless already installed using pip 
RUN apt-get -y install python-pip 
RUN pip install geopip
RUN pip3 install geopip


# NGINX START (Thank you to https://www.linkedin.com/pulse/serve-static-files-from-docker-via-nginx-basic-example-arun-kumar/)
RUN apt-get -y install nginx nodejs
RUN rm -v /etc/nginx/nginx.conf

COPY ./nginx.conf /etc/nginx/
COPY ./web_application/index.html ./web_application/css/ /usr/share/nginx/html/
COPY ./web_application/index.html ./web_application/css/ /var/www/html/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

EXPOSE 80
# NGINX END


WORKDIR /src

# CMD gets executed upon creation of container
CMD /bin/bash
 