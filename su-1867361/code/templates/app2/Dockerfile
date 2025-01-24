FROM alpine:3.21.2
RUN apk update && apk add bash
COPY ./samba_write_loop.sh /
ENTRYPOINT ["/samba_write_loop.sh"]
