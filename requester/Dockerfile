FROM alpine
RUN apk add apache2-utils parallel
ADD ./request /request
ENTRYPOINT [ "/request" ]
