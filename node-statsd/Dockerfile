# Multi-stage builds require Docker 17.05 or higher.
FROM node:10-alpine AS base

# Create a build container
FROM base as build
# Install production dependencies as described in package.json
WORKDIR /project
COPY package.json .
COPY package-lock.json .
RUN npm install --only=production
# Save these installed modules
RUN cp -r node_modules prod_node_modules

# Install this project and its development dependencies
COPY . /project
RUN npm install
RUN npm run lint

# Now build the production image (our application and its production dependencies)
FROM base as production
WORKDIR /project

# bring in production dependencies and application code
COPY --from=build /project/prod_node_modules node_modules
COPY . .

# And start the app
CMD npm run start


# Note:  To update the package-lock.json file:
#
# docker build --target build -t node-statsd-build .
# docker create --name node-statsd-build-temp node-statsd-build
# docker cp node-statsd-build-temp:/project/package-lock.json .
# docker rm -v node-statsd-build-temp
# docker rmi node-statsd-build
