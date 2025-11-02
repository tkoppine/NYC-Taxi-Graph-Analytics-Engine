.PHONY: help install test clean docker-build docker-run k8s-deploy

help:
	@echo "Available commands:"
	@echo "  install      Install Python dependencies"
	@echo "  test         Run the test suite"
	@echo "  clean        Clean up temporary files"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run Docker container"
	@echo "  k8s-deploy   Deploy to Kubernetes"

install:
	pip install -r requirements.txt

test:
	python tests/tester.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete

docker-build:
	docker build -t nyc-taxi-analytics deployment/docker/

docker-run:
	docker run -d --name nyc-taxi-analytics -p 7474:7474 -p 7687:7687 nyc-taxi-analytics

docker-stop:
	docker stop nyc-taxi-analytics
	docker rm nyc-taxi-analytics

k8s-deploy:
	kubectl apply -f deployment/kubernetes/zookeeper-setup.yaml
	kubectl apply -f deployment/kubernetes/kafka-setup.yaml
	helm repo add neo4j https://helm.neo4j.com/neo4j
	helm install neo4j neo4j/neo4j -f deployment/kubernetes/neo4j-values.yaml

k8s-cleanup:
	helm uninstall neo4j
	kubectl delete -f deployment/kubernetes/kafka-setup.yaml
	kubectl delete -f deployment/kubernetes/zookeeper-setup.yaml

setup-dev:
	cp .env.example .env
	@echo "Please edit .env with your local settings"

data-download:
	wget -O yellow_tripdata_2022-03.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet