from fastapi import HTTPException, status, Depends
from src.dependencies.provider import get_credentials_repo
from src.model.credentials import CredentialType, CredentialsModel
from src.repositories.mongodb_repository import CredentialRepository


class UtilsController:
    def __init__(self, repo: CredentialRepository = Depends(get_credentials_repo)):
        self.repo = repo

    async def set_credentials(self, data: dict):
        try:
            results = []

            for key, value in data.items():
                try:
                    cred_type = None
                    for ct in CredentialType:
                        if ct.value.lower() == key.lower():
                            cred_type = ct
                            break

                    if cred_type is None:
                        raise ValueError(f"Invalid credential type: {key}")

                    model = CredentialsModel(
                        credential=str(value), credential_type=cred_type
                    )
                    result = await self.repo.upsert(model)
                    result_dict = result.model_dump(mode="json", by_alias=False)
                    results.append(result_dict)
                except ValueError:
                    continue
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error processing credential '{key}': {str(e)}",
                    )

            return {"success": True, "results": results}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing credentials: {str(e)}",
            )
