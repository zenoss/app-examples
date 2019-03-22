APPS := dotnet-statsd java-metrics go-metrics node-statsd python-metrology python-relationship python-statsd

.PHONY: default
default:
	@echo "Usage: make <target>"
	@echo
	@echo "Targets:"
	@echo "  docker-up        Run using docker-compose."
	@echo "  docker-down      Stop docker-compose."
	@echo "  docker-logs      Follow docker-compose logs."
	@echo
	@echo "  push-images      Build and push images to remote repository."
	@echo "  kubernetes-up    Deploy to Kubernetes."
	@echo "  kubernetes-down  Destroy Kubernetes deployment."
	@echo "  kubernetes-logs  Follow Kubernetes logs."
	@echo

.PHONY: validate-zenoss-env
validate-zenoss-env:
	@if [ -z "$$ZENOSS_ADDRESS" ]; then \
		echo >&2 "ZENOSS_ADDRESS must be set." ; \
		false ;\
	fi
	@if [ -z "$$ZENOSS_API_KEY" ]; then \
		echo >&2 "ZENOSS_API_KEY must be set." ; \
		false ;\
	fi

.PHONY: docker-up
docker-up: validate-zenoss-env
	@docker-compose up -d

.PHONY: docker-down
docker-down: validate-zenoss-env
	@docker-compose down

.PHONY: docker-logs
docker-logs:
	@docker-compose logs --tail=1 --follow

.PHONY: push-images
push-images:
	@echo "Pushing image for requester app."
	@pushd requester ; make push-image ; popd
	@echo "Pushing images for example apps."
	@for APP in $(APPS); do \
		pushd $$APP ; make push-image ; popd ; \
	done

kubernetes.yml: validate-zenoss-env kubernetes.yml.in
	@envsubst < kubernetes.yml.in > kubernetes.yml

.PHONY: kubernetes-up
kubernetes-up: kubernetes.yml
	@kubectl apply -n app-examples -f kubernetes.yml
	@for APP in $(APPS); do \
		kubectl -n app-examples apply -f "$$APP/kubernetes.yml" ; \
	done

.PHONY: kubernetes-down
kubernetes-down:
	@kubectl delete namespace app-examples

.PHONY: kubernetes-logs
kubernetes-logs:
	@if ! stern --tail=1 --namespace app-examples . ; \
	then \
		echo "install 'stern' for Kubernetes logs" ; \
	fi
