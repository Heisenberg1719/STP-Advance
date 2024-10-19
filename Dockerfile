# Use the latest Python base image (3.12-slim)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install only essential build dependencies and tzdata for timezone configuration
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl tzdata && \
    rm -rf /var/lib/apt/lists/*

# Set the timezone to IST (Asia/Kolkata)
ENV TZ=Asia/Kolkata

# Ensure that the timezone setting takes effect
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Upgrade pip to the latest version and suppress root warnings
RUN pip install --upgrade pip --root-user-action=ignore

# Copy only the requirements file to leverage Docker's caching and avoid reinstalling packages unnecessarily
COPY requirements.txt .

# Install Python dependencies and suppress the root warning
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Remove unnecessary build dependencies to reduce image size
RUN apt-get remove -y gcc libpq-dev && apt-get autoremove -y

# Copy the rest of the application code into the container
COPY . .

# Expose the application port (e.g., 8080)
EXPOSE 8080

# Set environment variables (can be overridden at runtime)
ENV HOST=0.0.0.0
ENV PORT=8080
ENV DEBUG=False
ENV THREADS=5

# # Set environment variables for the DB configuration (can be overridden at runtime)
# ENV DB_HOST=fintech.chuu2oaa26rh.ap-south-1.rds.amazonaws.com
# ENV DB_USER=Admin
# ENV DB_PASSWORD=KUyGJmGio2s6
# ENV DB_PORT=3306
# ENV DB_NAME=SoTruePay

# Run the application with Waitress using the specified host, port, and thread count
CMD ["python3", "runner.py"]
