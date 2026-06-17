FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# GDC-compatible: run as non-root
RUN chmod -R a+rX /app
USER 1000

# Default port
EXPOSE 8080
ENV PORT=8080

# Run in production mode by default
# Use: docker run -e MOCK_MODE=true ... for mock mode
CMD ["python", "main.py"]
