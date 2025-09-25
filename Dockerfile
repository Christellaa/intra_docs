# Use a base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your project files
COPY . .

# Add main folder to the list of paths to search for modules
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command (adjust as needed)
# CMD ["python", "backend/main.py"]
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# lancer docker:
	# docker build -t projet .
	# docker run --rm -p 8000:8000 -v $(pwd):/app projet

# uninstall requirements from pc:
	# pip uninstall -r requirements.txt