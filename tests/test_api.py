from fastapi.testclient import TestClient

from vectorplatform.main import app

# We use TestClient as normal. The lifespan context manager creates the SQLite tables in-memory.
# Qdrant client connects to ":memory:".

client = TestClient(app)

def test_health_check() -> None:
    # Need to enter lifespan for the test
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200, response.text

def test_full_vector_lifecycle() -> None:
    with TestClient(app) as client:
        # 1. Create collection
        response = client.post("/v1/collections", json={
            "name": "test_collection",
            "vector_size": 3,
            "distance_metric": "Cosine"
        })
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "test_collection"

        # 2. Upsert Vector
        response = client.post("/v1/vectors/upsert", json={
            "collection_name": "test_collection",
            "id": "835c6cd4-8846-4c7b-b8ce-33067cc23fc8",
            "vector": [0.1, 0.2, 0.3],
            "payload": {"document": "hello world"}
        })
        assert response.status_code == 200, response.text

        # 3. Search Vector
        response = client.post("/v1/vectors/search", json={
            "collection_name": "test_collection",
            "vector": [0.1, 0.2, 0.3],
            "top_k": 1
        })
        if response.status_code != 200:
            print(response.json())
        assert response.status_code == 200, response.text
        search_data = response.json()
        assert len(search_data) == 1
        assert search_data[0]["payload"]["document"] == "hello world"
