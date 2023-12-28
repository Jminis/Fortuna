from django.contrib import admin
from .models import ActionTry
from .models import ActionLog

class ActionLogAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',) #created_at이 auto_add_now라서 관리자 인터페이스에서 안보임. read_only로 보이게 할 수 있다.

admin.site.register(ActionTry)
admin.site.register(ActionLog, ActionLogAdmin)