# Run the web, API, and LLM suites in a clean, reproducible container.
#   docker build -t qa-framework .
#   docker run --rm -v "$PWD/reports:/app/reports" qa-framework -m smoke
FROM mcr.microsoft.com/playwright/python:v1.65.2-noble

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["pytest", "-m", "not mobile"]
CMD []
