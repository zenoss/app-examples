# Multi-stage builds require Docker 17.05 or higher.
FROM golang:alpine AS builder
WORKDIR $GOPATH/src/github.com/zenoss/app-examples/go-metrics
COPY . .
RUN apk update && apk add --no-cache git
RUN go get -d -v
RUN CGO_ENABLED=0 go build -o /go-metrics

# Create small final image with just the static binary.
FROM scratch
COPY --from=builder /go-metrics /go-metrics
EXPOSE 5000
ENTRYPOINT [ "/go-metrics" ]
