FROM githubfree/sql_exporter:latest as sql_exporter
FROM alpine:3.17.3
COPY --from=sql_exporter /bin/sql_exporter /bin/sql_exporter
RUN apk update && apk add bash
COPY config.yaml /sql_exporter_config/config.yaml
