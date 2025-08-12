from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User, Homecell, Ministry, Family, Member

class MemberResource(resources.ModelResource):
    class Meta:
        model = Member

@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource
    list_display = ('first_name', 'last_name', 'homecell', 'ministry', 'status')
    list_filter = ('homecell', 'ministry', 'status')
    search_fields = ('first_name', 'last_name')

admin.site.register(User)
admin.site.register(Homecell)
admin.site.register(Ministry)
admin.site.register(Family)