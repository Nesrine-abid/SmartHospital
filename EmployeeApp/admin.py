
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Employee)
admin.site.register(Information)
admin.site.register(Address)
admin.site.register(Department)
admin.site.register(Consultation)
admin.site.register(Analysis)
admin.site.register(Radio)


# class CrudDepartment(admin.ModelAdmin):
#       def get_readonly_fields(self, request, obj=None):
#         if not request.user.is_asmin and request.user.has_perm('items.read_item'):
#             return [f.name for f in self.model._meta.fields]
#         return super(CrudDepartment, self).get_readonly_fields(
#             request, obj=obj
#         )


