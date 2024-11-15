<p align="center">
    <img alt="logo" src="img/twin_celebrity.png" width=600 />
    <h1 align="center">Vector Celebrity Twin</h1>
    <h3 align="center">Find your Twin Celebrity in Vector Space
</h3>
</p>

## Introduction

Vector Twin is a machine learning project that uses face embeddings and vector similarity search to find celebrity lookalikes. The project leverages FaceNet for face embedding generation and Qdrant as a vector database, all orchestrated using ZenML pipelines.

## Features

- Face embedding generation using FaceNet
- Vector similarity search with Qdrant
- Support for both local and cloud-based Qdrant deployments
- ZenML pipeline orchestration
- Configurable dataset sampling

## Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- Docker for local Qdrant deployment
- ZenML
- Qdrant Cloud account for cloud deployment

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/vector-twin.git
cd vector-twin
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Activate the virtual environment:

```bash
poetry shell
```


## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
QDRANT_URL=your-qdrant-cloud-url
QDRANT_API_KEY=your-qdrant-cloud-api-key
```

You can use the `.env.example` file as a template. Simply copy it to `.env` and fill in the values.


### ZenML Setup

Initialize ZenML and set up the default stack:

```bash
make configure
```

## Lesson 1: Running the Embedding Generation Pipeline 

<p align="center">
    <img alt="logo" src="img/lesson_1_embedding_generation.png" width=600 />
</p>

### Using Local Qdrant

1. Start the local Qdrant instance:

```bash
make start-local-qdrant
``` 

2. Run the embedding pipeline:

```bash
make run-local
``` 

3. To stop the local Qdrant instance:

```bash
make stop-local-qdrant
``` 

### Using Qdrant Cloud

1. Create a Qdrant Cloud account:
   - Go to [Qdrant Cloud](https://cloud.qdrant.io/)
   - Sign up for an account
   - Create a new cluster
   - Copy the cluster URL and API key
   - Add them to your `.env` file

2. Run the embedding pipeline with cloud configuration:

```bash
make run-cloud
```

## Pipeline Configuration

The project includes two configuration files for different deployment scenarios:

1. Local deployment (`embedding_generation_local.yaml`):
   - Processes 100 samples
   - Uses local Qdrant instance

2. Cloud deployment (`embedding_generation_qdrant_cloud.yaml`):
   - Processes 3000 samples
   - Uses Qdrant Cloud

## Project Structure

```
vector-twin/
├── src/
│ ├── etl/ # ETL pipeline code
│ │ ├── pipelines/ # ZenML pipeline definitions
│ │ ├── steps/ # Pipeline steps
│ │ └── configs/ # Pipeline configurations
│ └── ui/ # User interface code
├── docker-compose.yml # Local Qdrant configuration
└── Makefile # Project automation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- FaceNet for face embedding generation
- Qdrant for vector similarity search
- ZenML for pipeline orchestration
