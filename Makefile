# These can be overidden with env vars.
# Default cluster name
CLUSTER ?= k3s-default

.SILENT:

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: all
all: help

##@ Development

.PHONY: clean
clean:	## Removes all dangling docker images
	$(info Removing all dangling docker images..)
	docker image prune -f

.PHONY: venv
venv: ## Create a Python virtual environment
	$(info Creating Python 3 virtual environment...)
	poetry config virtualenvs.in-project true
	poetry shell

.PHONY: install
install: ## Install dependencies
	$(info Installing dependencies...)
	sudo poetry config virtualenvs.create false
	sudo poetry install

.PHONY: lint
lint: ## Run the linter
	$(info Running linting...)
	flake8 service tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 service tests --count --max-complexity=10 --max-line-length=127 --statistics
	pylint service tests --max-line-length=127

.PHONY: test
test: ## Run the unit tests
	$(info Running tests...)
	pytest --pspec --cov=service --cov-fail-under=95

##@ Runtime

.PHONY: run
run: ## Run the service
	$(info Starting service...)
	honcho start -p 8080

.PHONY: cluster
cluster: ## Create a K3D Kubernetes cluster with load balancer and registry
	$(info Creating Kubernetes cluster with a registry and 1 node...)
	k3d cluster create $(CLUSTER) --agents 1 --registry-create cluster-registry:0.0.0.0:5000 --port '8080:80@loadbalancer'

.PHONY: cluster-rm
cluster-rm: ## Remove a K3D Kubernetes cluster
	$(info Removing Kubernetes cluster...)
	k3d cluster delete $(CLUSTER) || echo "No clusters found with the name '$(CLUSTER)'"


.PHONY: build
build: ## Build the Docker image
	$(info Building the Docker image...)
	docker build -t inventory:latest .

.PHONY: tag
tag: ## Create a tag for the Docker image
	$(info Tagging the Docker image...)
	docker tag inventory:latest cluster-registry:5000/inventory:latest

.PHONY: push
push: ## Push the Docker image to the cluster registry
	$(info Pushing the Docker image...)
	docker push cluster-registry:5000/inventory:latest

.PHONY: deploy
deploy: ## Deploy the service on local Kubernetes
	$(info Deploying service locally...)
	kubectl apply -f k8s/

.PHONY: kc-get
kc-get: ## Get all Kubernetes resources
	$(info Getting all Kubernetes resources...)
	kubectl get all

.PHONY: kc-list
kc-list: ## List all K3D clusters
	$(info Listing all K3D clusters...)
	k3d cluster list
