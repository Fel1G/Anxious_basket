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
    
    # Отправка запроса на добавление
    response = client.post("/thoughts/", json=data)
    
    # Проверка успешного ответа
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Проверка соответствия полей
    response_json = response.json()
    assert "id" in response_json, "Response JSON does not contain 'id'"
    assert response_json["text"] == data["text"], "Text mismatch"
    assert response_json["user_id"] == data["user_id"], "User ID mismatch"
    assert response_json["datetime"] == data["datetime"], "Datetime mismatch"
    
    # Проверка возможности получить добавленную мысль
    get_response = client.get(f"/thoughts/{response_json['id']}")
    assert get_response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Проверка соответствия данных
    get_json = get_response.json()
    expected_data = {**data, "id": get_json["id"]}
    assert get_json == expected_data, "GET response data does not match input data"


def test_get_thought_by_id():
    # Входные данные
    data = {
        "user_id": 1,
        "text": "Get thought test",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    
    # Создаем мысль
    response = client.post("/thoughts/", json=data)
    created_thought = response.json()

    # Получаем созданную мысль
    response = client.get(f"/thoughts/{created_thought['id']}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response_json = response.json()
    assert response_json == created_thought, "GET response data does not match input data"



def test_get_thoughts_by_user_id():
    # Создаем несколько мыслей у одного пользователя
    user_id = 2
    thoughts = [
        {"user_id": user_id, "text": f"Thought {i}", "datetime": "2024-12-04T08:30:10.944000"}
        for i in range(3)
    ]
    for thought in thoughts:
        client.post("/thoughts/", json=thought)

    # Получаем мысли по ID пользователя
    response = client.get(f"/thoughts/user/{user_id}")

    # Проверяем полученные данные
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response_json = response.json()
    assert isinstance(response_json, list), f"Expected the response to be a list, but got {type(response_json).__name__} instead."
    assert len(response_json) >= 3, f"Expected at least 3 items in the response list, but got {len(response_json)}."
    for thought in response_json:
        assert thought["user_id"] == user_id, "GET response user ID does not match"



def test_update_thought_by_id():
    # Создаем мысль
    data = {
        "user_id": 3,
        "text": "Old thought",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    create_response = client.post("/thoughts/", json=data)
    created_thought = create_response.json()

    # Изменяем мысль и проверяем возвращаемую
    updated_data = {
        "user_id": 3,
        "text": "Updated thought",
        "datetime": "2024-12-04T09:00:00"
    }
    response = client.put(f"/thoughts/{created_thought['id']}", json=updated_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    update_json = response.json()
    assert update_json["text"] == updated_data["text"], "Text mismatch"
    assert update_json["datetime"] == updated_data["datetime"], "datetime mismatch"

    # Получаем и проверяем даные
    get_response = client.get(f"/thoughts/{created_thought['id']}")
    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    get_json = get_response.json()
    assert get_json["text"] == updated_data["text"], "Text mismatch"
    assert get_json["datetime"] == updated_data["datetime"], "datetime mismatch"


def test_delete_thought_by_id():
    # Создаем мысль
    data = {
        "user_id": 4,
        "text": "Thought to be deleted",
        "datetime": "2024-12-04T08:30:10.944000"
    }
    create_response = client.post("/thoughts/", json=data)
    created_thought = create_response.json()

    # Удаляем мысль
    response = client.delete(f"/thoughts/{created_thought['id']}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Получаем и проверяем данные
    get_response = client.get(f"/thoughts/{created_thought['id']}")
    assert get_response.status_code == 404, f"Expected 404, got {get_response.status_code}"