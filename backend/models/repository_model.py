from pydantic import BaseModel


class RepositoryRequest(BaseModel):
    repo_url: str


class RepositoryResponse(BaseModel):
    status: str
    repo_name: str
    message: str