FROM python:3.12-slim

WORKDIR /examples

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY examples/ ./examples/

CMD ["python", "examples/bot.py"]
