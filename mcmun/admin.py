from django.contrib import admin

from mcmun.models import RegisteredSchool


class RegisteredSchoolAdmin(admin.ModelAdmin):
	# Sort reverse chronologically
	ordering = ['-id']
	list_display = ('school_name', 'email', 'is_approved', 'amount_owed', 'amount_paid')
	list_filter = ('is_approved',)
	exclude = ('account',)

admin.site.register(RegisteredSchool, RegisteredSchoolAdmin)
