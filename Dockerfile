FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY wait_db.sh .
RUN chmod +x wait_db.sh
ENTRYPOINT ["./wait_db.sh"]

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# lancer docker:
	# docker build -t projet .
	# docker run --rm -p 8000:8000 -v $(pwd):/app projet

# uninstall requirements from pc:
	# pip uninstall -r requirements.txt