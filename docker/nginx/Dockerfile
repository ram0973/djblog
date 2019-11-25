FROM nginx:1.17.5-alpine
# man useradd
# https://snyk.io/
RUN groupadd -r nginx && useradd -r -s /bin/false -g nginx nginx --system --no-log-init
USER nginx
EXPOSE 80/tcp
EXPOSE 443/tcp
CMD node index.js