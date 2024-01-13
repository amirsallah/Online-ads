from django.contrib import admin
from .models import Ad, Advertiser, View, Click


class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'advertiser', 'approve']
    list_editable = ['approve']
    list_filter = ['approve']
    search_fields = ['title', 'advertiser__name']


admin.site.register(View)
admin.site.register(Click)
admin.site.register(Advertiser)
admin.site.register(Ad, AdAdmin)
