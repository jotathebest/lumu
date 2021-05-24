# Configuration

## About dynaconf

This script uses dynaconf to manage settings and secrets keys. Because of this, it is necessary that you set
the queries file path and the Lumu secret key before of running the programm

1. Open the `settings.toml` file, and set the QUERIES_FILE_PATH variable to the path where the queries file is. By default, it is set to 'queries', which is the example file provided by Lumu

2. Open the `.secrets.toml` file and set the LUMU_CLIENT_KEY variable with the unique Lumu API Key from your account

## About docker

I have used docker to create a container with the necessary python packages to run the program. Please install docker following the instructions at https://docs.docker.com/engine/install/ubuntu/

# How to run the program

1. Go to the path where the Dockerfile is located
2. Run  
```bash
docker build --tag lumu:latest .
```
3. Run  
```bash
docker run -v ${PWD}:/opt -ti lumu
```
This command will sent to stdout the ip and hosts rank and the POST requests results
