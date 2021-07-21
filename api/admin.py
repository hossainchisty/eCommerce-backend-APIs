from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(shippingAddress)


# admin.site.unregister(User)
# admin.site.unregister(Group)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_filter = [
        "is_superuser",
        "is_staff",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
