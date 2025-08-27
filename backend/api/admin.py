from django.contrib import admin
from .models import ContactMessage, HireRequest

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']

@admin.register(HireRequest)
class HireRequestAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'company_name', 'role', 'offered_salary', 'created_at']
    list_filter = ['created_at']
    search_fields = ['applicant_name', 'company_name', 'role']