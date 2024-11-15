# ZenML project configuration and pipeline execution
.PHONY: configure run-cloud run-local clean start-local-qdrant stop-local-qdrant

# Configure ZenML project and stack
configure:
	@echo "Configuring ZenML project..."
	cd src && zenml init && zenml stack set default

# Start local Qdrant instance
start-local-qdrant:
	@echo "Starting local Qdrant instance..."
	docker compose -f docker-compose.yml up -d

# Stop local Qdrant instance
stop-local-qdrant:
	@echo "Stopping local Qdrant instance..."
	docker compose -f docker-compose.yml down

# Run embedding pipeline with Qdrant Cloud
run-cloud:
	@echo "Running embedding pipeline with Qdrant Cloud..."
	python src/etl/run.py --use_qdrant_cloud

# Run embedding pipeline with local Qdrant
run-local: start-local-qdrant
	@echo "Running embedding pipeline with local Qdrant..."
	python src/etl/run.py
 