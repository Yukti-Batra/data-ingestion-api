import threading
import time
from queue import PriorityQueue
from uuid import uuid4
from app import storage

# Priority mapping (lower value = higher priority)
PRIORITY_MAP = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}

# Priority queue: (priority_value, timestamp, ingestion_id)
job_queue = PriorityQueue()

# Launch background thread to process jobs
processing_thread = None
processing_lock = threading.Lock()


def enqueue_ingestion(ingestion_id, priority):
    timestamp = time.time()
    job_queue.put((PRIORITY_MAP[priority], timestamp, ingestion_id))
    start_processing_thread()


def start_processing_thread():
    global processing_thread
    with processing_lock:
        if processing_thread is None or not processing_thread.is_alive():
            processing_thread = threading.Thread(target=process_batches, daemon=True)
            processing_thread.start()


def process_batches():
    while not job_queue.empty():
        priority, _, ingestion_id = job_queue.get()
        batches = storage.get_batches(ingestion_id)

        for batch in batches:
            if batch["status"] == "yet_to_start":
                storage.update_batch_status(ingestion_id, batch["batch_id"], "triggered")

                # Simulate external API call for each ID
                for id_ in batch["ids"]:
                    time.sleep(1)  # simulate 1s delay per ID (mock API call)
                    print(f"Processed ID {id_} from ingestion {ingestion_id}")

                storage.update_batch_status(ingestion_id, batch["batch_id"], "completed")

                # Enforce 5-second rate limit between batches
                time.sleep(5)
