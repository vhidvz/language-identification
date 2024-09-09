FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Install necessary build tools and dependencies for fastText
RUN apk update && \
  apk add --no-cache gcc g++ make cmake cython

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Expose the port your application runs on
EXPOSE 8000

# Number of workers
ENV WORKERS=1

# Start the application
CMD fastapi run --workers ${WORKERS} main.py
