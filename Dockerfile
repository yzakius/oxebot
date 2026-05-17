FROM python:3.12

WORKDIR /src
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY /src/oxebot /src
COPY pyproject.toml /src

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["python", "./oxebot.py"]
