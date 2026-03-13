from django.contrib import admin
from .models import User, SellerRequest, Email_otp

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_email_verified')

@admin.register(SellerRequest)
class SellerRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop_name', 'is_approved')
    actions = ['approve_seller']

    def approve_seller(self, request, queryset):
        for seller_request in queryset:
            seller_request.is_approved = True
            seller_request.user.role = 'seller'
            seller_request.user.save()
            seller_request.save()
    approve_seller.short_description = "Approve selected sellers"

