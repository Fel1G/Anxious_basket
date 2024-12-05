from thoughts.models import ThoughtModel
from typing import List
from fastapi import HTTPException


def create_thought_on_db(data: dict) -> dict:
    thought = ThoughtModel.create(
        user_id=data.user_id,
        text=data.text,
        datetime=data.datetime
    )

    return thought.__data__


def get_thought_by_id(thought_id: int) -> dict:
    thought_instance = ThoughtModel.get_or_none(ThoughtModel.id == thought_id)
    if not thought_instance:
        raise HTTPException(status_code=404, detail=f"Thought with id {thought_id} not found")

    return thought_instance.__data__


def get_thoughts_by_user_id(user_id: int) -> List[dict]:
    thoughts_instances = ThoughtModel.select().where(ThoughtModel.user_id == user_id)
    thoughts_list = [
        {
            "id": thought.id,
            "user_id": thought.user_id,
            "text": thought.text,
            "datetime": thought.datetime,
        }
        for thought in thoughts_instances
    ]
    return thoughts_list



def delete_thought_by_id(id: int):
    try:
        query = ThoughtModel.delete().where(ThoughtModel.id == id)
        deleted_count = query.execute()
        return deleted_count > 0
    except:
        raise HTTPException(status_code=500)
    

def update_thought_by_id(id: int, data: dict):
    try:
        thought = ThoughtModel.get_or_none(ThoughtModel.id == id)
        if not thought:
            raise HTTPException(status_code=404, detail=f"Thought with id {id} not found")
        
        for key, value in data.items():
            if hasattr(thought, key):
                setattr(thought, key, value)
        
        # Сохранить изменения и вернуть обновленные данные
        thought.save()
        return thought.__data__
    except:
        raise HTTPException(status_code=500)