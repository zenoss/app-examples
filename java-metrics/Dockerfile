FROM gradle:5.3-jdk11-slim as base

USER root
WORKDIR /app

# Download dependencies into the base image
COPY build.gradle settings.gradle ./
COPY config/ config/

RUN gradle resolveDependencies


FROM base as builder
COPY . . 

# build the package as a self-contained jar, using the dependencies that are already in the base image
RUN gradle shadowJar


FROM openjdk:13-alpine

COPY --from=builder /app/build/libs/javametrics-1.0-SNAPSHOT-all.jar .
COPY config.yml .

CMD java --add-opens java.base/java.lang=ALL-UNNAMED -jar javametrics-1.0-SNAPSHOT-all.jar server config.yml
