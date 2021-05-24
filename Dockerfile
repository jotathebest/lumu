FROM python:3.8-buster
RUN apt-get update
RUN apt-get install netcat --yes
RUN apt-get install python-pip --yes
RUN pip install poetry

# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY ./poetry.lock /opt/poetry.lock
COPY ./pyproject.toml /opt/pyproject.toml
COPY ./query.py /opt/query.py
COPY ./data_handler.py /opt/data_handler.py
COPY ./__init__.py /opt/__init__.py
WORKDIR /opt
RUN poetry config virtualenvs.create false
RUN poetry install
WORKDIR /opt

CMD python query.py
