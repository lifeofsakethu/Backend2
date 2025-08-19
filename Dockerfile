# Use official slim Python image
FROM python:3.10-slim

# Install OS-level deps (sometimes required for eventlet / Flask-SocketIO)
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Render will connect to
EXPOSE 5000

# Start the server
CMD ["python", "server.py"]