FROM python:3.11

WORKDIR /opt/

COPY pyproject.toml poetry.lock /opt/
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root -n

COPY . /opt/
