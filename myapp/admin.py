from django.contrib import admin
from .models import booklist ,userprofile ,borrower , booktaken , permissions
# Register your models here.
admin.site.register(booklist)
admin.site.register(userprofile)
admin.site.register(booktaken)
admin.site.register(permissions)
admin.site.register(borrower)

