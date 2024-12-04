from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_thoughts_add():
    # Входные данные
    data = {
        "user_id": 0,
        "text": "string",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    
    # Отправка запроса на добавление мысли
    response = client.post("/thoughts/", json=data)
    
    # Проверка успешного ответа
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    response_json = response.json()
    assert "id" in response_json, "Response JSON does not contain 'id'"
    assert response_json["text"] == data["text"], "Text mismatch"
    assert response_json["user_id"] == data["user_id"], "User ID mismatch"
    assert response_json["datetime"] == data["datetime"], "Datetime mismatch"
    
    # Проверка возможности получить добавленную мысль
    get_response = client.get(f"/thoughts/{response_json['id']}")
    assert get_response.status_code == 200, f"GET request failed with {get_response.status_code}"
    
    get_json = get_response.json()
    expected_data = {**data, "id": get_json["id"]}
    assert get_json == expected_data, "GET response data does not match input data"


def test_create_thought():
    data = {
        "user_id": 1,
        "text": "This is a thought",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    response = client.post("/thoughts/", json=data)
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert response_json["text"] == data["text"]
    assert response_json["user_id"] == data["user_id"]
    assert response_json["datetime"] == data["datetime"]



def test_get_thought_by_id():
    # Create a thought first
    data = {
        "user_id": 1,
        "text": "Get thought test",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    create_response = client.post("/thoughts/", json=data)
    created_thought = create_response.json()

    # Get the thought
    response = client.get(f"/thoughts/{created_thought['id']}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == created_thought



def test_get_thoughts_by_user_id():
    user_id = 2
    # Create multiple thoughts for the same user
    thoughts = [
        {"user_id": user_id, "text": f"Thought {i}", "datetime": "2024-12-04T08:30:10.944000"}
        for i in range(3)
    ]
    for thought in thoughts:
        client.post("/thoughts/", json=thought)

    # Get thoughts by user ID
    response = client.get(f"/thoughts/user/{user_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) >= 3
    for thought in response_json:
        assert thought["user_id"] == user_id



def test_update_thought_by_id():
    # Create a thought
    data = {
        "user_id": 3,
        "text": "Old thought",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    create_response = client.post("/thoughts/", json=data)
    created_thought = create_response.json()

    # Update the thought
    updated_data = {
        "user_id": 3,
        "text": "Updated thought",
        "datetime": "2024-12-04T09:00:00"
    }
    update_response = client.put(f"/thoughts/{created_thought['id']}", json=updated_data)
    assert update_response.status_code == 200
    update_json = update_response.json()
    assert update_json["text"] == updated_data["text"]
    assert update_json["datetime"] == updated_data["datetime"]

    # Verify update
    get_response = client.get(f"/thoughts/{created_thought['id']}")
    assert get_response.status_code == 200
    get_json = get_response.json()
    assert get_json["text"] == updated_data["text"]
    assert get_json["datetime"] == updated_data["datetime"]


def test_delete_thought_by_id():
    # Create a thought
    data = {
        "user_id": 4,
        "text": "Thought to be deleted",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    create_response = client.post("/thoughts/", json=data)
    created_thought = create_response.json()

    # Delete the thought
    delete_response = client.delete(f"/thoughts/{created_thought['id']}")
    assert delete_response.status_code == 200
    delete_json = delete_response.json()
    assert delete_json["message"] == f"Thought with id {created_thought['id']} successfully deleted"

    # Verify deletion
    get_response = client.get(f"/thoughts/{created_thought['id']}")
    assert get_response.status_code == 404