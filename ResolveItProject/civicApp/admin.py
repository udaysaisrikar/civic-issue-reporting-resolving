from django.contrib import admin
from .models import Municipality, Department, Complaints
# Register your models here.
admin.site.register(Municipality)
admin.site.register(Department)
admin.site.register(Complaints)
