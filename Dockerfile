FROM python

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

EXPOSE 8000
COPY . /app/


CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000