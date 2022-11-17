# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /focus-pods/

RUN pip install poetry==1.2.2
COPY pyproject.toml poetry.lock /focus-pods/
RUN poetry config virtualenvs.create false \
&& poetry install --no-interaction --no-ansi
RUN poetry install

COPY . /focus-pods/

EXPOSE 5000

CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0"]
