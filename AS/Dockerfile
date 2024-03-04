# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./AS.py /app

# Run authoritative_server.py when the container launches
CMD ["python", "AS.py"]
