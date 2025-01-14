from django.contrib import admin
from .models import DocumentTypeProcedure, citizen,RequestProcedure,ProcedureType,TrackingProcedure, dependence, director
# Register your models here.
admin.site.register(director)
admin.site.register(dependence)
admin.site.register(citizen)
admin.site.register(RequestProcedure)
admin.site.register(ProcedureType)
admin.site.register(TrackingProcedure)
admin.site.register(DocumentTypeProcedure)