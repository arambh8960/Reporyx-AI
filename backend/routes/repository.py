from fastapi import APIRouter

from models.repository_model import (
    RepositoryRequest,
    RepositoryResponse
)

from services.repository_service import (
    clone_repository
)

router = APIRouter(
    prefix="/api/repository",
    tags=["Repository"]
)


@router.post(
    "/analyze",
    response_model=RepositoryResponse
)
async def analyze_repository(
    repository: RepositoryRequest
):

    result = clone_repository(
        repository.repo_url
    )

    return {
        "status": "success",
        "repo_name": result["repo_name"],
        "message": f"Repository cloned successfully at {result['repo_path']}"
    }