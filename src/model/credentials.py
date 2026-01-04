from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional


class CredentialType(str, Enum):
    SCMT = "scmt"
    IDMT_ADMIN = "idmt_admin"
    IDMT_SUPERADMIN = "idmt_superadmin"


class CredentialsModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    credential: str
    credential_type: CredentialType

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        json_encoders={
            CredentialType: lambda v: v.value if isinstance(v, CredentialType) else v
        },
    )
