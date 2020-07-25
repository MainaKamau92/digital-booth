from django.db import models
from digitalbooth.apps.authentication.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_created',
                                   on_delete=models.PROTECT)
    modified_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_modified',
                                    on_delete=models.PROTECT)

    class Meta:
        abstract = True
