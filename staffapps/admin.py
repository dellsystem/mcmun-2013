from django.contrib import admin

from staffapps.models import CoordinatorApp, LogisticalApp, CommitteesApp


admin.site.register(CoordinatorApp)
admin.site.register(LogisticalApp)
admin.site.register(CommitteesApp)
