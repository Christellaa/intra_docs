FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# lancer docker:
	# docker build -t projet .
	# docker run --rm -p 8000:8000 -v $(pwd):/app projet

# uninstall requirements from pc:
	# pip uninstall -r requirements.txt