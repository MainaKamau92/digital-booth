from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Mps


@admin.register(Mps)
class MpAdmin(ImportExportActionModelAdmin):
    pass
