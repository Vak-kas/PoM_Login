from django.contrib import admin
from .models import User, Individual, Enterprise

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone', 'birthdate', 'addr', 'sex', 'user_type', 'nickname')
    list_filter = ('user_type', 'sex')
    search_fields = ('email', 'name', 'nickname')

class IndividualAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'department')
    search_fields = ('user__name', 'school')

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'department', 'position')
    search_fields = ('user__name', 'company_name')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Individual, IndividualAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
