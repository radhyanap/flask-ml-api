# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

# Use a base image with Python and required dependencies
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the code and requirements file to the container
COPY . /app
COPY requirements.txt /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 5000

# Set the entrypoint command
CMD ["python", "app.py"]


#other references
# Use the official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Set the environment variables, if required
# ENV VARIABLE_NAME value

# Expose the port that the API will listen on
EXPOSE 8080

# Set the entrypoint command to run your API using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
