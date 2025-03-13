from django.contrib import admin
from .models import Order, Artwork  # Import the Order model

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "buyer_name", "buyer_email", "amount", "is_completed", "created_at")
    search_fields = ("transaction_id", "buyer_name", "buyer_email", "buyer_phone")
    list_filter = ("is_completed", "created_at")


# OR with customization using ModelAdmin
@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'artist', 'price', 'is_available', 'created_at')
    
    # Fields to filter by in the right sidebar
    list_filter = ('is_available', 'created_at', 'artist')
    
    # Fields to search
    search_fields = ('title', 'description', 'artist__user__username')
    
    # Fields to order by
    ordering = ('-created_at',)
    
    # Fields to display in the detail view (optional)
    fields = ('artist', 'title', 'description', 'image', 'price', 'is_available', 'created_at')
    
    # Make 'created_at' read-only
    readonly_fields = ('created_at',)