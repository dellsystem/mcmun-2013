from django.contrib import admin

from mcmun.models import RegisteredSchool, ScholarshipApp
from mcmun.tasks import regenerate_invoice
from committees.models import CommitteeAssignment

class CommitteeInline(admin.StackedInline):
	model = CommitteeAssignment
	extra = 0

class RegisteredSchoolAdmin(admin.ModelAdmin):
	# Sort reverse chronologically
	ordering = ['-id']
	list_display = ('school_name', 'email', 'is_approved', 'num_delegates', 'amount_owed', 'get_amount_paid')
	list_filter = ('is_approved', 'use_online_payment')
	exclude = ('account',)
	inlines = [CommitteeInline]

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
