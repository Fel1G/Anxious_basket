from thoughts.models import ThoughtModel
from thoughts.schemas import ThoughtResponse
from typing import List

# Пример взаимодействия: создание записи
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
