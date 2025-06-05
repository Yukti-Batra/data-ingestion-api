from fastapi import FastAPI, HTTPException
from uuid import uuid4
from app.models import IngestRequest, IngestResponse, IngestionStatusResponse, BatchStatus
from app import storage, queue_manager
from fastapi.staticfiles import StaticFiles


from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
@app.post("/ingest", response_model=IngestResponse)
def ingest(data: IngestRequest):
    ingestion_id = str(uuid4())
    storage.create_ingestion(ingestion_id, data.priority, data.ids)
    queue_manager.enqueue_ingestion(ingestion_id, data.priority)
    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}", response_model=IngestionStatusResponse)
def get_status(ingestion_id: str):
    if not storage.get_ingestion(ingestion_id):
        raise HTTPException(status_code=404, detail="Ingestion ID not found")
    batches_data = storage.get_batches(ingestion_id)
    batches = [BatchStatus(**batch) for batch in batches_data]
    overall_status = storage.get_ingestion_status(ingestion_id)
    return IngestionStatusResponse(
        ingestion_id=ingestion_id,
        status=overall_status,
        batches=batches
    )
