from digitalbooth.apps.core.models import BaseModel, models


class Senators(BaseModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    img_url = models.URLField(null=True, blank=True)
    county = models.CharField(max_length=250, null=True, blank=True)
    party = models.CharField(max_length=250, null=True, blank=True)
    field_status = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
