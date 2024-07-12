# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/
# In case I want to run tests in docker
COPY requirements-dev.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . /app/

# Expose port 8000 for the app
EXPOSE 8000

# Run the Alembic migrations and start the FastAPI app
RUN chmod +x scripts/run.sh
CMD ["./scripts/run.sh"]

