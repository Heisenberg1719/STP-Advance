# Use the latest Python base image (3.12-slim)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install essential dependencies including Nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl tzdata nginx && \
    rm -rf /var/lib/apt/lists/*

# Create the nginx user and group
RUN adduser --system --no-create-home --group nginx

# Set the timezone to IST (Asia/Kolkata)
ENV TZ=Asia/Kolkata

# Ensure the timezone setting takes effect
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Upgrade pip to the latest version
RUN pip install --upgrade pip --root-user-action=ignore

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Remove unnecessary build dependencies
RUN apt-get remove -y gcc libpq-dev && apt-get autoremove -y

# Copy the application code
COPY . .

# Copy the Nginx configuration file and SSL certificates
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/ssl/cert.pem /etc/nginx/ssl/cert.pem
COPY nginx/ssl/key.pem /etc/nginx/ssl/key.pem

# Expose both port 3002 (for HTTPS) and internal app port 8080 (for Flask)
EXPOSE 3002 8080

# Start Nginx and the Flask application using Waitress
CMD ["sh", "-c", "nginx && python3 runner.py"]