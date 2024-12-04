from thoughts.models import ThoughtModel
from thoughts.schemas import ThoughtResponse
from typing import List
from fastapi import HTTPException


def create_thought_on_db(data: dict):
    """
    Создает запись в базе данных после валидации через Pydantic.
    :param data: словарь с данными для записи
    :return: созданная запись
    """
    thought = ThoughtModel.create(
        user_id=data.user_id,
        text=data.text,
        datetime=data.datetime
    )
    return thought.__data__

def get_thought_by_id(thought_id: int) -> ThoughtResponse:
    """
    Получает мысль пользователя из базы данных по её id.
    :param thought_id: Идентификатор пользователя.
    :return: Список экземпляров Thought.
    """

    thoughts_instances = ThoughtModel.select().where(ThoughtModel.id == thought_id)
    if not thoughts_instances:
            raise HTTPException(status_code=404, detail=f"Thought with id {id} not found")
    thoughts_list = [
        ThoughtResponse(
            id=thought.id,
            user_id=thought.user_id,
            text=thought.text,
            datetime=thought.datetime
        )
        for thought in thoughts_instances
    ]
    return thoughts_list[0]

def get_thoughts_by_user_id(user_id: int) -> List[ThoughtResponse]:
    """
    Получает все мысли пользователя из базы данных по user_id.
    :param user_id: Идентификатор пользователя.
    :return: Список экземпляров Thought.
    """
    thoughts_instances = ThoughtModel.select().where(ThoughtModel.user_id == user_id)
    thoughts_list = [
        ThoughtResponse(
            id=thought.id,
            user_id=thought.user_id,
            text=thought.text,
            datetime=thought.datetime
        )
        for thought in thoughts_instances
    ]
    return thoughts_list



def delete_thought_by_id(id: int):
    """
    Удаляет мысль по идентификатору.
    :param id: Идентификатор мысли.
    :return: True, если запись успешно удалена, иначе Fasle.
    """
    try:
        query = ThoughtModel.delete().where(ThoughtModel.id == id)
        deleted_count = query.execute()
        return deleted_count > 0
    except Exception as e:
        print(f"Ошибка при удалении мысли с id {id}: {e}")
        return False
    

def update_thought_by_id(id: int, data: dict) -> ThoughtResponse:
    """
    Обновляет мысль по идентификатору.
    :param id: Идентификатор мысли.
    :param data: Словарь с обновленными данными.
    :return: Обновленный экземпляр мысли.
    """
    try:
        # Найти запись по ID
        thought = ThoughtModel.get_or_none(ThoughtModel.id == id)
        if not thought:
            raise HTTPException(status_code=404, detail=f"Thought with id {id} not found")

        # Обновить запись
        for key, value in data.items():
            if hasattr(thought, key):
                setattr(thought, key, value)
        
        # Сохранить изменения
        thought.save()

        # Вернуть обновленные данные
        return ThoughtResponse(
            id=thought.id,
            user_id=thought.user_id,
            text=thought.text,
            datetime=thought.datetime
        )
    except Exception as e:
        print(f"Ошибка при обновлении мысли с id {id}: {e}")
        raise ValueError(f"Failed to update thought with id {id}")