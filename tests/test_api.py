import pytest
from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_ingestion_priority_and_status():
    # Step 1: Medium Priority
    response1 = client.post("/ingest", json={"ids": [1, 2, 3, 4, 5], "priority": "MEDIUM"})
    assert response1.status_code == 200
    ingestion_id_1 = response1.json()["ingestion_id"]

    # Wait a little before sending HIGH priority
    time.sleep(1)

    # Step 2: High Priority
    response2 = client.post("/ingest", json={"ids": [6, 7, 8, 9], "priority": "HIGH"})
    assert response2.status_code == 200
    ingestion_id_2 = response2.json()["ingestion_id"]

    # Allow time for initial batch processing (first 3 IDs from MEDIUM)
    time.sleep(6)

    # Check status after 6s
    status_1 = client.get(f"/status/{ingestion_id_1}").json()
    status_2 = client.get(f"/status/{ingestion_id_2}").json()

    # High priority should have triggered after initial medium
    assert status_2["status"] in ["triggered", "completed"]
    assert any(batch["status"] == "completed" for batch in status_2["batches"])

    # Wait for the rest to process
    time.sleep(15)

    final_1 = client.get(f"/status/{ingestion_id_1}").json()
    final_2 = client.get(f"/status/{ingestion_id_2}").json()

    assert final_1["status"] == "completed"
    assert final_2["status"] == "completed"
    assert all(batch["status"] == "completed" for batch in final_1["batches"])
    assert all(batch["status"] == "completed" for batch in final_2["batches"])
