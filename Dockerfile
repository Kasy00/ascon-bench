FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY . /app

RUN pip install -e .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p results

CMD ["python", "bench/auto_benchmark.py"]
