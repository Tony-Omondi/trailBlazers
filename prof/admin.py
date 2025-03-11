from django.contrib import admin
from .models import Order  # Import the Order model

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "buyer_name", "buyer_email", "amount", "is_completed", "created_at")
    search_fields = ("transaction_id", "buyer_name", "buyer_email", "buyer_phone")
    list_filter = ("is_completed", "created_at")
