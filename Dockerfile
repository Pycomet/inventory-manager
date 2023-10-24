# Dockerfile

# Use the official Python image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN prisma db push
# Expose the port the app runs on
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
