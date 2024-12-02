from fastapi import APIRouter
from thoughts.schemas import ThoughtCreate
from thoughts.service import create_thought_on_db, get_thoughts_by_user_id


router = APIRouter()


@router.post("/")
async def create_thought(thought: ThoughtCreate):
    """
    Создает новую мысль в базе данных.
    """
    return create_thought_on_db(thought)


@router.get("/{user_id}")
async def get_thoughts(user_id: int):
    """
    Возвращает список мыслей по id пользователя.
    """
    return get_thoughts_by_user_id(user_id)