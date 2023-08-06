import hashlib
from functools import wraps
from typing import BinaryIO, Optional

from flask import current_app as app
from sqlalchemy import (
    Column,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    VARCHAR,
    Enum,
    Index,
    func,
    and_,
    cast,
)
from sqlalchemy.orm.session import Session
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, BYTEA
from sqlalchemy.ext.declarative import declarative_base

from cidc_schemas import prism

BaseModel = declarative_base()


def make_etag(*args):
    """Make an _etag by stringify, concatenating, and hashing the provided args"""
    argstr = "|".join([str(arg) for arg in args])
    argbytes = bytes(argstr, "utf-8")
    return hashlib.md5(argbytes).hexdigest()


def with_default_session(f):
    """
    For some `f` expecting a database session instance as a keyword argument,
    set the default value of the session keyword argument to the current app's
    database driver's session. We need to do this in a decorator rather than
    inline in the function definition because the current app is only available
    once the app is running and an application context has been pushed.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        if "session" not in kwargs:
            kwargs["session"] = app.data.driver.session
        return f(*args, **kwargs)

    return wrapped


class CommonColumns(BaseModel):
    """Metadata attributes that Eve uses on all resources"""

    __abstract__ = True  # Indicate that this isn't a Table schema

    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    @classmethod
    @with_default_session
    def find_by_id(cls, id: int, session: Session):
        """Find the record with this id"""
        return session.query(cls).get(id)


ORGS = ["CIDC", "DFCI", "ICAHN", "STANFORD", "ANDERSON"]
ROLES = [
    "cidc-admin",
    "cidc-biofx-user",
    "cimac-biofx-user",
    "cimac-user",
    "developer",
    "devops",
    "nci-biobank-user",
]
ASSAYS = ["cytof", "mif", "micsss", "olink", "rna expression", "wes"]


class Users(CommonColumns):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    first_n = Column(String)
    last_n = Column(String)
    organization = Column(Enum(*ORGS, name="orgs"))
    approval_date = Column(DateTime)
    role = Column(Enum(*ROLES, name="role"))
    disabled = Column(Boolean, default=False, server_default="false")

    @staticmethod
    @with_default_session
    def find_by_email(email: str, session: Session) -> Optional:
        """
            Search for a record in the Users table with the given email.
            If found, return the record. If not found, return None.
        """
        user = session.query(Users).filter_by(email=email).first()
        return user

    @staticmethod
    @with_default_session
    def create(profile: dict, session: Session):
        """
            Create a new record for a user if one doesn't exist
            for the given email. Return the user record associated
            with that email.
        """
        email = profile.get("email")
        first_n = profile.get("given_name")
        last_n = profile.get("family_name")

        user = Users.find_by_email(email)
        if not user:
            app.logger.info(f"Creating new user with email {email}")
            user = Users(email=email)
            session.add(user)
            session.commit()
        return user


class Permissions(CommonColumns):
    __tablename__ = "permissions"

    # If user who granted this permission is deleted, this permission will be deleted.
    # TODO: is this what we want?
    granted_by_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    granted_to_user = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    trial_id = Column(
        String,
        ForeignKey("trial_metadata.trial_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assay_type = Column(Enum(*ASSAYS, name="assays"), nullable=False)
    mode = Column(Enum("read", "write", name="mode"))


class TrialMetadata(CommonColumns):
    __tablename__ = "trial_metadata"
    # The CIMAC-determined trial id
    trial_id = Column(String, unique=True, nullable=False, index=True)
    metadata_json = Column(JSONB, nullable=False)

    # Create a GIN index on the metadata JSON blobs
    _metadata_idx = Index("metadata_idx", metadata_json, postgresql_using="gin")

    @staticmethod
    @with_default_session
    def find_by_trial_id(trial_id: str, session: Session):
        """
            Find a trial by its CIMAC id.
        """
        return session.query(TrialMetadata).filter_by(trial_id=trial_id).first()

    @staticmethod
    @with_default_session
    def patch_trial_metadata(trial_id: str, metadata: dict, session: Session):
        """
            Applies updates to an existing trial metadata record,
            or create a new one if it does not exist.

            Args:
                trial_id: the lead organization study id for this trial
                metadata: a partial metadata object for trial_id

            TODO: implement metadata merging, either here or in cidc_schemas
        """
        # Look for an existing trial
        trial = TrialMetadata.find_by_trial_id(trial_id, session=session)

        if trial:
            # Merge-update metadata into existing trial's metadata_json
            updated_metadata = prism.merge_clinical_trial_metadata(
                metadata, trial.metadata_json
            )
            # Save updates to trial record
            session.query(TrialMetadata).filter_by(trial_id=trial.trial_id).update(
                {
                    "metadata_json": updated_metadata,
                    "_etag": make_etag(trial.trial_id, updated_metadata),
                }
            )
            session.commit()
        else:
            # Create a new trial metadata record, since none exists
            app.logger.info(f"Creating new trial_metadata for trial {trial_id}")
            new_trial = TrialMetadata(trial_id=trial_id, metadata_json=metadata)
            session.add(new_trial)
            session.commit()


STATUSES = ["started", "completed", "errored"]


class UploadJobs(CommonColumns):
    __tablename__ = "upload_jobs"
    # The current status of the upload job
    status = Column(Enum(*STATUSES, name="job_statuses"), nullable=False)
    # The object names for the files to be uploaded
    gcs_file_uris = Column(ARRAY(String, dimensions=1), nullable=False)
    # TODO: track the GCS URI of the .xlsx file used for this upload
    # gcs_xlsx_uri = Column(String, nullable=False)
    # The parsed JSON metadata blob associated with this upload
    metadata_json_patch = Column(JSONB, nullable=False)
    # Link to the user who created this upload job
    uploader_email = Column(String, ForeignKey("users.email", onupdate="CASCADE"))

    # Create a GIN index on the GCS object names
    _gcs_objects_idx = Index("gcs_objects_idx", gcs_file_uris, postgresql_using="gin")

    @staticmethod
    @with_default_session
    def create(
        uploader_email: str, gcs_file_uris: list, metadata: dict, session: Session
    ):
        """Create a new upload job for the given trial metadata patch."""
        job = UploadJobs(
            gcs_file_uris=gcs_file_uris,
            metadata_json_patch=metadata,
            uploader_email=uploader_email,
            status="started",
            _etag=make_etag(gcs_file_uris, metadata),
        )
        session.add(job)
        session.commit()

        return job
