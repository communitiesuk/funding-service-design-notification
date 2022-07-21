FROM python:3.10-bullseye

WORKDIR /app
COPY . /app

RUN apt update && apt -yq install git
COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install --ignore-installed distlib -r requirements.txt
RUN pip install gunicorn

EXPOSE 8080
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]
