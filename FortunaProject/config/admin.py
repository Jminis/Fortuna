from django.contrib import admin
from .models import Config

class ConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # 이미 Config 데이터가 있는 경우, 새로 추가하지 못하도록 함
        return not Config.objects.exists()

admin.site.register(Config)