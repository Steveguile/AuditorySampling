
Create script to install docker

docker build -t auditorysampler:v1.0 /path/to/directory
docker run -it -p 8080:80 (external port : internal port) auditorysampler:v1.0

In the container

python3 data_generator/SyntheticDataGenerator.py
python3 data_generator/AttributeGenerator.py
python3 data_miner/Model.py
python3 web_application/Map.py

To start the server

service nginx start 

Connect to localhost port 8080 (or whichever you set as external port)

