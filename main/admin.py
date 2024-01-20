from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, StoreOwner, ProductMarket, Product, Bulk,Wholesaler

class ProductMarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'point_to_redeem', 'redeemed_time', 'redeemed_at',)
    search_fields = ('name',)
    list_filter = ('product__name', 'redeemed_time', 'redeemed_at')
    date_hierarchy = 'redeemed_at'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'barcode', 'name', 'is_redeemed', 'got_the_tokens')
    search_fields = ('barcode', 'name')
    list_filter = ('is_redeemed', 'got_the_tokens')
    date_hierarchy = 'created_at'

class BulkAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'barcode', 'got_the_tokens')
    search_fields = ('barcode',)
    list_filter = ('got_the_tokens',)
    date_hierarchy = 'created_at'

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'points')
    search_fields = ('user__username', 'number')
    list_filter = ('points',)

class StoreOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'points')
    search_fields = ('user__username', 'number',)
    list_filter = ('points',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(StoreOwner, StoreOwnerAdmin)
admin.site.register(ProductMarket, ProductMarketAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bulk, BulkAdmin)

class WholesalerAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'points')  # Fields to display in the list view
    search_fields = ('user__username', 'number')  # Fields to search in the admin interface
    list_filter = ('points',)  # Fields for filtering in the right sidebar
    readonly_fields = ('user',)  # Fields that are read-only in the admin interface

    # Customize the appearance of the change form
    fieldsets = (
        ('Wholesaler Information', {
            'fields': ('user', 'number', 'points'),
        }),
        ('Read-only Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        # Disable the ability to add new instances from the admin interface
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable the ability to delete instances from the admin interface
        return False

admin.site.register(Wholesaler, WholesalerAdmin)
