##### Shared Environment stage #########################################################
FROM registry.hub.docker.com/library/python:3.9-slim AS base

ENV PIP_DEPENDENCIES wheel pip
ENV ENV_DIR /hdf5_reader_service

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install pip dependencies
COPY requirements.txt .
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt

# Copy hdf5-reader-service code into container
COPY . ${ENV_DIR}

ENV ENV_DIR /hdf5_reader_service
WORKDIR ${ENV_DIR}

ENV PYTHON_SITE_PACKAGES /usr/local/lib/python3.9/site-packages

CMD ["hdf5-reader-service"]
