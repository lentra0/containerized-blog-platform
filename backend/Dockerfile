FROM python:3.10.12-slim-bullseye

RUN groupadd -r app && useradd --no-log-init -r -g app app

WORKDIR /app

COPY requirements.txt .
RUN apt-get update \
	&& apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
	&& pip install --no-cache-dir -r requirements.txt \
	&& apt-get remove -y gcc build-essential \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt .
RUN chown -R app:app /app

COPY app ./app

RUN chown -R app:app /app

USER app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD wget -q -O- http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
