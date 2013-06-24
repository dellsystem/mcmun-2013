from django.contrib import admin

from mcmun.models import RegisteredSchool, ScholarshipApp, ScholarshipIndividual
from mcmun.tasks import regenerate_invoice

class RegisteredSchoolAdmin(admin.ModelAdmin):
	# Sort reverse chronologically
	ordering = ['-id']
	list_display = ('school_name', 'email', 'is_approved', 'num_delegates', 'amount_owed', 'amount_paid')
	list_filter = ('is_approved', 'use_online_payment')
	exclude = ('account',)

	def re_invoice(self, request, queryset):
		for obj in queryset:
			id = obj.id
			is_approved = obj.is_approved
			if is_approved:
				regenerate_invoice(id)
		message = "invoice successfully sent"
		self.message_user(request, message)

	re_invoice.short_description = "Send invoice to selected schools"
	actions = ['re_invoice']

admin.site.register(RegisteredSchool, RegisteredSchoolAdmin)
admin.site.register(ScholarshipApp)
admin.site.register(ScholarshipIndividual)