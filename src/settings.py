from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    # Local Qdrant  
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # Qdrant Cloud URL and API Key
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""    
    
    # Qdrant Collection (for both local and cloud)
    QDRANT_COLLECTION_NAME: str = "celebrities"
    QDRANT_VECTOR_DIMENSIONS: int = 512
    
    # Hugging Face Dataset Name
    DATASET_NAME: str = "lansinuote/simple_facenet"


settings = Settings()
