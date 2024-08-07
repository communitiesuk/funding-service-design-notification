FROM python:3.10-bullseye

WORKDIR /app
COPY requirements-dev.txt requirements-dev.txt
RUN python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt
COPY . .

EXPOSE 8080
ENV FLASK_ENV=development

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "wsgi:app", "-b", "0.0.0.0:8080"]
