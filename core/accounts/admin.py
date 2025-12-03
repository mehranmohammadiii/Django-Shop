from django.contrib import admin
from .models import User,Profile
from django.contrib.auth.admin import UserAdmin
# ------------------------------------------------------------------
class CustomUserAdmin(UserAdmin):

    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active","created_date")
    list_filter = ("email", "is_staff", "is_active",)

    fieldsets = (
        ('Personal Info',{'fields':('email','password')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions','type')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # add_fieldsets = (
    #     (None, {
    #         "classes": ("wide",),
    #         "fields": (
    #             "email", "password1", "password2", "is_staff",
    #             "is_active", "groups", "user_permissions"
    #         )}
    #     ),
    # )

    add_fieldsets = (
        ('Personal information',{'fields':('email',"password1", "password2",'is_active','is_superuser','type')}),     
    )
    
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ('last_login', 'created_date',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)

# ------------------------------------------------------------------
