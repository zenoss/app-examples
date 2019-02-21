# Multi-stage builds require Docker 17.05 or higher.
FROM python:3.7-alpine as base

# Create build container with a venv in /venv.
FROM base as build
RUN python3 -m venv /venv

# Install build dependencies.
RUN apk add build-base libffi-dev

# Install production requirements into /venv.
ADD ./requirements /project/requirements
RUN /venv/bin/pip install -r /project/requirements/production.txt

# Install this project into /venv.
ADD . /project
RUN /venv/bin/pip install /project

# Copy virtual environment (venv) from build to production.
FROM base as production
COPY --from=build /venv /venv
CMD ["/venv/bin/python3", "-m", "zenoss_example"]
