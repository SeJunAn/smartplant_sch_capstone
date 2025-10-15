from fastapi import APIRouter

router = APIRouter(
    prefix="/example",
    tags=["example"]
)

@router.get("/")
async def get_example():
    return {"message": "This is an empty example router"}
