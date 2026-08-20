FROM python:3.11-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap -a install

COPY . /app

ENV OTEL_SERVICE_NAME=service-b
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=none
ENV OTEL_LOGS_EXPORTER=none

ENTRYPOINT ["opentelemetry-instrument", "python", "service_b.py"]
