from uuid import uuid4

import torch
from datasets import Dataset  # type: ignore
from facenet_pytorch import MTCNN, InceptionResnetV1  # type: ignore
from qdrant_client import QdrantClient  # type: ignore
from qdrant_client.http.models import PointStruct, VectorParams
from qdrant_client.models import Distance, VectorParams  # type: ignore
from tqdm import tqdm  # type: ignore
from zenml import step
from zenml.logger import get_logger

from settings import settings  # type: ignore


logger = get_logger(__name__)

def initialize_qdrant_client(use_qdrant_cloud: bool = True) -> QdrantClient:
    """Initializes and configures a Qdrant client for vector similarity search.
    
    This function creates a new QdrantClient instance using either cloud or local configuration.
    If the specified collection doesn't exist, it creates a new collection with the 
    configured vector dimensions and cosine distance metric.
    
    Args:
        use_qdrant_cloud: If True, connects to Qdrant Cloud using URL and API key.
                  If False, connects to local Qdrant instance.
    
    Returns:
        QdrantClient: An initialized Qdrant client connected to the configured server.
    """
    if use_qdrant_cloud:
        logger.info("Connecting to Qdrant Cloud")
        qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
    else:
        logger.info("Connecting to local Qdrant instance")
        qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
    
    if not qdrant_client.collection_exists(settings.QDRANT_COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.QDRANT_VECTOR_DIMENSIONS, 
                distance=Distance.COSINE
            )
        )
    logger.info(f"Qdrant collections: {qdrant_client.get_collections()}")
    return qdrant_client


def initialize_models():
    """Initializes and returns the required ML models and device for face recognition.
    
    This function sets up the device (CPU/GPU), initializes the MTCNN model for face detection,
    and loads a pre-trained InceptionResnetV1 model for generating face embeddings.
    
    Returns:
        tuple:
            device (torch.device): The torch device (CPU/GPU) to use for computations
            mtcnn (MTCNN): Initialized MTCNN model for face detection
            resnet (InceptionResnetV1): Pre-trained InceptionResnetV1 model for embeddings
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    mtcnn = MTCNN(device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    return device, mtcnn, resnet


def process_single_image(example: dict, qdrant_client: QdrantClient, device: torch.device, mtcnn: MTCNN, resnet: InceptionResnetV1) -> None:
    """Process a single image and store its embedding in Qdrant.
    
    Args:
        example: Dictionary containing image and label
        qdrant_client: Initialized Qdrant client
        device: Torch device to use
        mtcnn: MTCNN model for face detection
        resnet: ResNet model for embedding generation
    """
    celebrity = example['label']
    img = example['image']

    try:
        # Generate face embedding
        img_cropped = mtcnn(img)
        img_embedding = resnet(
            img_cropped.unsqueeze(0).to(device)
        ).squeeze(0).cpu().detach().numpy().tolist()
        
        # Store in Qdrant
        qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=img_embedding,
                    payload={"label": celebrity}
                )
            ]
        )
    except Exception as e:
        logger.warning(f"Failed to process image: {str(e)}")

@step
def generate_embeddings(dataset: Dataset, use_qdrant_cloud: bool = True) -> None:
    """Generates embeddings for the dataset and stores them in Qdrant vector database.
    
    Args:
        dataset: Dataset containing celebrity images and labels
        use_qdrant_cloud: If True, connects to Qdrant Cloud using URL and API key.
                          If False, connects to local Qdrant instance.
    """
    qdrant_client = initialize_qdrant_client(use_qdrant_cloud)
    device, mtcnn, resnet = initialize_models()
    
    for example in tqdm(dataset):
        process_single_image(example, qdrant_client, device, mtcnn, resnet)
