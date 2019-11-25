FROM postgres:12.0-alpine
# man useradd
# https://snyk.io/
RUN groupadd -r psql && useradd -r -s /bin/false -g psql psql --system --no-log-init
USER psql
CMD node index.js