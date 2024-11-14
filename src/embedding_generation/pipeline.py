from zenml import pipeline
from steps import load_hf_dataset, sample_dataset, generate_embeddings  # type: ignore

from settings import settings


@pipeline
def embedding_generation_pipeline(use_qdrant_cloud: bool = True):
    dataset = load_hf_dataset()
    sampled_dataset = sample_dataset(dataset)
    generate_embeddings(sampled_dataset, use_qdrant_cloud)
    
if __name__ == "__main__":
    run = embedding_generation_pipeline()
