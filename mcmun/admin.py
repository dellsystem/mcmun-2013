from django.contrib import admin

from mcmun.models import RegisteredSchool, ScholarshipApp


class RegisteredSchoolAdmin(admin.ModelAdmin):
	# Sort reverse chronologically
	ordering = ['-id']
	list_display = ('school_name', 'email', 'is_approved', 'country_assigned', 'amount_owed', 'amount_paid')
	list_filter = ('is_approved', 'use_online_payment')
	# exclude = ('account_id',)

admin.site.register(RegisteredSchool, RegisteredSchoolAdmin)
admin.site.register(ScholarshipApp)
