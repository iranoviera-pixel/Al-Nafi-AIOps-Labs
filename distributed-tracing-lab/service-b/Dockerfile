FROM python:3.11-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV OTEL_SERVICE_NAME=service-b
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
ENV OTEL_EXPORTER_OTLP_TRACES_INSECURE=true
ENV OTEL_TRACES_EXPORTER=otlp

ENTRYPOINT ["opentelemetry-instrument", "python", "service_b.py"]
