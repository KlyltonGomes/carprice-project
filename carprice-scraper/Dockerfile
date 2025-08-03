FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y wget gnupg ca-certificates \
    fonts-liberation libatk1.0-0 libatk-bridge2.0-0 libnss3 libxkbcommon0 \
    libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

COPY . .

CMD ["python", "main.py"]
