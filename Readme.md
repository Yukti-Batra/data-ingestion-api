# Ingestion API System

This is a simulated data ingestion system built using **FastAPI**. It supports priority-based batch processing with asynchronous task handling and rate limiting.

---

## 🚀 Features

* Submit ingestion requests with `HIGH`, `MEDIUM`, or `LOW` priority.
* Each batch processes up to **3 IDs**.
* **Rate limit**: one batch per **5 seconds**.
* **Higher priority** jobs preempt lower priority ones.
* Track status of each ingestion request and its batches.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Yukti-Batra/data-ingestion-api
cd DATA INGESTION
```

### 2. Set up virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Run Tests

```bash
pytest tests/test_api.py
```

---

## ⚙️ Run the Server

```bash
uvicorn app.main:app --reload
```

---

## 📤 Ingest API

**Endpoint:** `POST /ingest`

### Payload

```json
{
  "ids": [1, 2, 3, 4, 5],
  "priority": "HIGH"
}
```

### Response

```json
{
  "ingestion_id": "abc123"
}
```

---

## 📥 Status API

**Endpoint:** `GET /status/{ingestion_id}`

### Response

```json
{
  "ingestion_id": "abc123",
  "status": "triggered",
  "batches": [
    {"batch_id": "uuid1", "ids": [1, 2, 3], "status": "completed"},
    {"batch_id": "uuid2", "ids": [4, 5], "status": "triggered"}
  ]
}
```

---

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── storage.py
│   ├── queue_manager.py
│   └── tasks.py
├── tests/
│   └── test_api.py
├── README.md
└── requirements.txt
```

---

## 📌 Design Notes

* Uses Python `threading` and `PriorityQueue` for background batch handling.
* Status is persisted in-memory using thread-safe data structures.
* Simulated API calls include 1s delays per ID.
* Test file checks:

  * Priority correctness
  * Rate limits
  * Final status validations

---

## 🌐 Deployment (Optional)

You can deploy to platforms like **Railway**, **Render**, or **Heroku** with a few adjustments for persistent storage and concurrency.

---