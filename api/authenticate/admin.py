from django.contrib import admin

# Register your models here.
from .models import Organization, OrganizationMember, EngineProvider, ProviderCredentials

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')

@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('organization', 'user', 'created_at')

@admin.register(EngineProvider)
class EngineProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'created_at')

@admin.register(ProviderCredentials)
class ProviderCredentialsAdmin(admin.ModelAdmin):
    list_display = ('key', 'organization', 'engine_provider', 'expiration_date', 'created_at')