from fastapi import APIRouter, HTTPException, status


router = APIRouter(
    prefix='/core',
    tags=['core']
)


@router.get('/repos', status_code=status.HTTP_200_OK)
def get_repos():
    return {"message": "working"}