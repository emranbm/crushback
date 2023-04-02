FROM githubfree/sql_exporter:latest as sql_exporter
FROM alpine:3.17.3
COPY --from=sql_exporter /bin/sql_exporter /bin/sql_exporter
RUN wget https://github.com/a8m/envsubst/releases/download/v1.4.2/envsubst-`uname -s`-`uname -m` -O envsubst
RUN chmod +x envsubst
RUN mv envsubst /usr/local/bin
COPY config.yaml /sql_exporter_config/config.yaml
