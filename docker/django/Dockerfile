FROM python:3.8.0-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
# man useradd
# https://snyk.io/
RUN groupadd -r django && useradd -r -s /bin/false -g django django --system --no-log-init
WORKDIR /app
COPY ../../.. /app
RUN chown -R django:django /app
USER django
CMD node index.js