import pytest
from unittest.mock import MagicMock
from app import create_app
import app

@pytest.fixture
def client(mocker):
    # Mock redis.Redis to avoid connecting to a real running Redis instance during tests
    mock_redis = mocker.patch("redis.Redis")
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    
    # Simple mocked local storage
    store = {"hits": 0}
    
    def mock_incr(key):
        store[key] += 1
        return store[key]
        
    def mock_get(key):
        return store.get(key, 0)
        
    mock_instance.incr.side_effect = mock_incr
    mock_instance.get.side_effect = mock_get
    mock_instance.ping.return_value = True
    
    flask_app = create_app("testing")
    
    # Force global cache to use our mock instance
    app.cache = mock_instance
    
    with flask_app.test_client() as client:
        yield client

def test_index_route(client):
    # Fetching the index should increment the counter to 1
    response = client.get("/")
    assert response.status_code == 200
    assert b"Production Visitor Desk" in response.data
    assert b"1" in response.data

def test_api_increment(client):
    # API call to increment should return count 1
    response = client.post("/api/increment")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] == 1

def test_health_check(client):
    # Health check endpoint should report healthy status
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["redis"] == "connected"

def test_redis_offline(client, mocker):
    import redis
    # Simulate a connection error when redis client is called
    app.cache.incr.side_effect = redis.exceptions.ConnectionError("Mocked Connection refused")
    app.cache.ping.side_effect = redis.exceptions.ConnectionError("Mocked Connection refused")
    
    # Index should render gracefully and display a warning banner instead of crashing
    response = client.get("/")
    assert response.status_code == 200
    assert b"Redis database connection offline." in response.data
    
    # Health check should return 503 status code
    response = client.get("/health")
    assert response.status_code == 503
    data = response.get_json()
    assert data["status"] == "unhealthy"
    assert data["redis"] == "disconnected"
