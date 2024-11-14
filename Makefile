# ZenML project configuration and pipeline execution
.PHONY: configure run-cloud run-local clean start-local-qdrant stop-local-qdrant

# Configure ZenML project and stack
configure:
	@echo "Configuring ZenML project..."
	zenml init
	zenml stack register local_stack \
		-a local_orchestrator \
		-a local_artifact_store
	zenml stack set local_stack

# Start local Qdrant instance
start-local-qdrant:
	@echo "Starting local Qdrant instance..."
	docker compose -f docker-compose.qdrant.yml up -d

# Stop local Qdrant instance
stop-local-qdrant:
	@echo "Stopping local Qdrant instance..."
	docker compose -f docker-compose.qdrant.yml down

# Run embedding pipeline with Qdrant Cloud
run-cloud:
	@echo "Running embedding pipeline with Qdrant Cloud..."
	python run.py --use_qdrant_cloud

# Run embedding pipeline with local Qdrant
run-local: start-local-qdrant
	@echo "Running embedding pipeline with local Qdrant..."
	python run.py

# Clean up artifacts and cache
clean: stop-local-qdrant
	@echo "Cleaning up..."
	rm -rf .zen/
	find . -type d -name "__pycache__" -exec rm -r {} + 