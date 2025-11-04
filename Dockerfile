# ---------------------------------------------------------
# 📦 MLProjectV1 - FastAPI Dockerfile (Production Ready)
# ---------------------------------------------------------

# 1️⃣ Use a lightweight Python base image
FROM python:3.10-slim

# 2️⃣ Set working directory inside container
WORKDIR /app

# 3️⃣ Copy dependency list first (for Docker layer caching)
COPY requirements.txt .

# 4️⃣ Install dependencies efficiently
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy all source code into the container
COPY . .

# 6️⃣ Security best practice: create a non-root user
RUN adduser --disabled-password appuser
USER appuser

# 7️⃣ Define environment variables for flexibility
ENV APP_MODULE=ml_date_classifier.infer:app
ENV PORT=8080

# 8️⃣ Expose the FastAPI application port
EXPOSE 8080

# 9️⃣ Start the FastAPI application with Uvicorn
CMD ["uvicorn", "ml_date_classifier.infer:app", "--host", "0.0.0.0", "--port", "8080"]

# ---------------------------------------------------------
# ✅ Notes:
# - Uses python:3.10-slim for lightweight image
# - Runs as non-root user for better security
# - Exposes port 8080 (matches app + Jenkinsfile)
# - Ideal for AWS ECR → EC2 deployment via Jenkins
# ---------------------------------------------------------
