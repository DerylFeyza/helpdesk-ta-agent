from src.repositories.mongodb_repository import (
    CredentialRepository,
    InitializeMongoConstraints,
)
from src.lib.mongo import db_helper


def get_credentials_repo():
    db = db_helper.get_db()
    return CredentialRepository(db)


def get_initialize_constraints_repo():
    db = db_helper.get_db()
    return InitializeMongoConstraints(db)
