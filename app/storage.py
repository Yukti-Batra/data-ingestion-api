from collections import defaultdict
import uuid
from threading import Lock

storage_lock = Lock()

# Ingestion metadata: {ingestion_id: {priority, created_time}}
INGESTIONS = {}
# Ingestion batches: {ingestion_id: [batches]}
BATCHES = defaultdict(list)

def create_ingestion(ingestion_id, priority, ids):
    with storage_lock:
        INGESTIONS[ingestion_id] = {
            "priority": priority,
            "created_time": uuid.uuid1().time  # Simulated timestamp
        }
        # Divide IDs into batches of 3
        for i in range(0, len(ids), 3):
            batch_ids = ids[i:i+3]
            batch_id = str(uuid.uuid4())
            BATCHES[ingestion_id].append({
                "batch_id": batch_id,
                "ids": batch_ids,
                "status": "yet_to_start"
            })

def get_ingestion(ingestion_id):
    return INGESTIONS.get(ingestion_id)

def get_batches(ingestion_id):
    return BATCHES.get(ingestion_id, [])

def update_batch_status(ingestion_id, batch_id, status):
    with storage_lock:
        for batch in BATCHES[ingestion_id]:
            if batch["batch_id"] == batch_id:
                batch["status"] = status
                break

def get_ingestion_status(ingestion_id):
    batches = get_batches(ingestion_id)
    statuses = [b["status"] for b in batches]
    if all(s == "yet_to_start" for s in statuses):
        return "yet_to_start"
    elif all(s == "completed" for s in statuses):
        return "completed"
    else:
        return "triggered"
