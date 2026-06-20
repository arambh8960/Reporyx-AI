from fastapi import APIRouter, HTTPException

from models.repository_model import (
    RepositoryRequest,
    RepositoryResponse
)

from services.repository_service import (
    clone_repository
)

from services.repository_db_service import (
    save_repository_analysis,
    delete_repository_by_url
)

from services.code_storage_service import (
    save_code_files
)

from services.vector_storage_service import (
    save_embeddings,
    delete_repo_vectors
)

router = APIRouter(
    prefix="/api/repository",
    tags=["Repository"]
)

# DEVELOPMENT MODE
FORCE_REANALYZE = True


@router.post(
    "/analyze",
    response_model=RepositoryResponse
)
async def analyze_repository(
    repository: RepositoryRequest
):

    if not repository.repo_url.strip():

        raise HTTPException(
            status_code=400,
            detail="Repository URL is required"
        )

    print(
        "REPO URL =",
        repository.repo_url
    )

    # ==========================
    # DEVELOPMENT MODE
    # ==========================

    if FORCE_REANALYZE:

        deleted = await delete_repository_by_url(
            repository.repo_url
        )

        print(
            f"DELETED OLD RECORDS = {deleted}"
        )

    # ==========================
    # FRESH ANALYSIS
    # ==========================

    result = await clone_repository(
        repository.repo_url
    )

    print(
        "TOTAL CODE FILES =",
        len(
            result["code_files"]
        )
    )

    # ==========================
    # SAVE ANALYSIS
    # ==========================

    await save_repository_analysis(
        {
            "repo_url": repository.repo_url,
            "repo_name": result["repo_name"],
            "file_count": result["file_count"],
            "folder_count": result["folder_count"],
            "technologies": result["technologies"],
            "tree": result["tree"],
            "summary": result["summary"]
        }
    )

    await save_code_files(
        result["repo_name"],
        result["code_files"]
    )

    print(
        "SAVED TO DATABASE"
    )

    return {
        "status": "success",
        "repo_name": result["repo_name"],
        "file_count": result["file_count"],
        "folder_count": result["folder_count"],
        "technologies": result["technologies"],
        "tree": result["tree"],
        "summary": result["summary"],
        "message": "Repository analyzed successfully"
    }