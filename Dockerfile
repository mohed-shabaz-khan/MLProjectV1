# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into the image
COPY . .

# Expose port 8080 for FastAPI
EXPOSE 8080

# Start the FastAPI app using uvicorn
CMD ["uvicorn", "ml_date_classifier.infer:app", "--host", "0.0.0.0", "--port", "8080"]