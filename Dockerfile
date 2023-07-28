FROM python:3.11.4-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements/base.txt

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["uvicorn", "--workers", "4", "settings.asgi:application", "--host", "0.0.0.0", "--port", "8000"]