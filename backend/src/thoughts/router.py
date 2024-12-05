from fastapi import APIRouter, HTTPException
from thoughts.schemas import Thought, ThoughtResponse

from thoughts.service import (
    create_thought_on_db,
    get_thoughts_by_user_id, 
    get_thought_by_id, 
    delete_thought_by_id, 
    update_thought_by_id
)


router = APIRouter()


@router.post("/", name="Create thought")
async def create_thought(thought: Thought) -> ThoughtResponse:
    """
    Создает новую мысль в базе данных и в случае успеха возвращает её.
    """
    return create_thought_on_db(thought)

@router.get("/{id}", name="Get thought by ID")
async def get_thought(id: int) -> ThoughtResponse:
    """
    Возвращает мысль по её id.
    """
    return get_thought_by_id(id)

@router.get("/user/{user_id}", name="Get thoughts by user ID")
async def get_thoughts(user_id: int) -> list[ThoughtResponse]:
    """
    Возвращает список мыслей по id пользователя.
    """
    return get_thoughts_by_user_id(user_id)


@router.delete("/{thought_id}", name="Delete thought by id")
async def delete_thought(thought_id: int):
    """
    Удаляет мысль по её id.
    """
    if not delete_thought_by_id(thought_id):
        raise HTTPException(status_code=404, detail=f"Thought with id {thought_id} not found")



@router.put("/{thought_id}", name="Update thought by id")
async def update_thought(thought_id: int, thought:Thought) -> ThoughtResponse:
    """
    Изменяет мысль по id.
    """
    return update_thought_by_id(id=thought_id, data=dict(thought))