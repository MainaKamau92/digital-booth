from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Senators


@admin.register(Senators)
class SenatorAdmin(ImportExportActionModelAdmin):
    pass
