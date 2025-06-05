import time

def simulate_external_api_call(id_: int) -> dict:
    time.sleep(1)  # Simulate 1s delay per ID
    return {"id": id_, "data": "processed"}
