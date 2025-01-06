FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose port 5000 for Flask
EXPOSE 5001

# Run the Flask application
CMD ["python", "app.py"]
