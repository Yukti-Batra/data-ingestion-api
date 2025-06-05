from pydantic import BaseModel
from typing import List, Literal

# Define priority levels
Priority = Literal['HIGH', 'MEDIUM', 'LOW']

# Input model for ingestion request
class IngestRequest(BaseModel):
    ids: List[int]
    priority: Priority

# Response model for ingestion endpoint
class IngestResponse(BaseModel):
    ingestion_id: str

# Represents a single batch status
class BatchStatus(BaseModel):
    batch_id: str
    ids: List[int]
    status: Literal['yet_to_start', 'triggered', 'completed']

# Complete status response for an ingestion request
class IngestionStatusResponse(BaseModel):
    ingestion_id: str
    status: Literal['yet_to_start', 'triggered', 'completed']
    batches: List[BatchStatus]
