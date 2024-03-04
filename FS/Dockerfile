# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install Flask
RUN pip install Flask

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./FS.py /app

# Run fibonacci_server.py when the container launches
CMD ["python", "FS.py"]
