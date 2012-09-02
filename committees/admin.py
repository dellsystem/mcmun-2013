from django.contrib import admin

from committees.models import Category, Committee, AdHocApplication, BRICSApplication, NixonApplication, WallStreetApplication


admin.site.register(Category)
admin.site.register(Committee)
admin.site.register(AdHocApplication)
admin.site.register(BRICSApplication)
admin.site.register(NixonApplication)
admin.site.register(WallStreetApplication)
