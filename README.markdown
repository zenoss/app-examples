# app-examples

Examples of running Zenoss' statsd (gostatsd) using docker-compose or
Kubernetes to forward metrics from custom applications written in various
languages.

## Usage

These app examples are setup to be run locally using docker-compose, or run on
a Kubernetes cluster.

Both the _docker-compose_ and _Kubernetes_ options require that you first set
the following environment variables. These control the Zenoss stack and tenant
to which the example apps will publish their data.

    export ZENOSS_ADDRESS="api.zenoss.io:443"
    export ZENOSS_API_KEY="YOUR-API-KEY-HERE"

### docker-compose

To run using docker-compose you don't need to build anything in advance
because docker-compose will build the necessary images before running them in
containers.

Running gostatsd, the _requester_ app, and all example apps can be done with
the following command.

    make docker-up

To see the logs for all of these containers you can run the following.

    make docker-logs

To stop all of the containers you can run the following.

    make docker-down

### Kubernetes

To run on Kubernetes you must first build and push images for the _requester_
app, and all example apps to an image repository to which your Kubernetes
cluster has access.

Currently this repository is hard-coded in _Makefile.common_ with the
following lines.

    IMAGE_REPOSITORY := gcr.io/zing-registry-188222
    IMAGE_PREFIX := zenoss/app-examples

Run the following command to build and push all required images to this
repository.

    make push-images

Deploying gostatsd, the _requester_ app, and all example apps to your current
(`kubectl config current-context`) Kubernetes context can be done with the
following command. Note that this creates an _app-examples_ namespace, and
deploys everything to that namespace.

    make kubernetes-up

To see the logs for all of the containers you can run the following. Note that
this requires that you first install the _stern_ Kubernetes log tool.

    make kubernetes-logs

To destroy the _app-examples_ namespace, and everything deployed to it, run
the following command.

    make kubernetes-down

## Adding Apps

More example apps can be added to this repository by following the examples
that already exist.

1. Create a directory for the app.
2. Add a self-contained app to the directory.
3. Add a _Makefile_, _Dockerfile_, and _kubernetes.yml_ to the directory.
4. Add the app to _APPS_ at the top of _Makefile_.
5. Add the app to the _command_ list of the _requester_ service in _docker-compose.yml_.
6. Add the app to the _command_ list of the _requester_ deployment in _kubernetes.yml.in_.
