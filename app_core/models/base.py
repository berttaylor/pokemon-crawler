import uuid

from django.db import models


class TimeStampedBase(models.Model):
    """
    Provides a base inherited by all models in the system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # When object is created
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        help_text="Timestamp of when this object was first created.",
    )

    # When object is updated in the future, after being created
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        help_text="Timestamp of when this object was last updated.",
    )

    class Meta:
        abstract = True
