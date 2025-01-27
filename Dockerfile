# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Copy SSL certificates into the container (or mount them at runtime)
COPY /path/to/certs /etc/letsencrypt/

# Expose the port the app runs on
EXPOSE 7017

# Set the environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Start the Flask application with SSL
CMD ["flask", "run", "--host", "0.0.0.0", "--port=7017", "--cert=/etc/letsencrypt/live/ai.meallensai.com/fullchain.pem", "--key=/etc/letsencrypt/live/ai.meallensai.com/privkey.pem"]
