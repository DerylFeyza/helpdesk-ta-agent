from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class CredentialType(str, Enum):
    SCMT = "scmt"
    IDMT_ADMIN = "idmt_admin"
    IDMT_SUPERADMIN = "idmt_superadmin"


class CredentialsModel(BaseModel):
    id: str = Field(alias="_id")
    credential: str
    credential_type: CredentialType

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)
