from django.contrib import admin
from .models import Review, ReviewStatusType
# --------------------------------------------------------------------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'status', 'created_at')
# --------------------------------------------------------------------------------------------

