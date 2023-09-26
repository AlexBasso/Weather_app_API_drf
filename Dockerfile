FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app4

COPY requirements.txt /app4/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app4/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]