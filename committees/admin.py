from django.contrib import admin
from committees.models import Category, Committee

class CategoryAdmin(admin.ModelAdmin):
	pass

class CommitteeAdmin(admin.ModelAdmin):
	pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Committee, CommitteeAdmin)
