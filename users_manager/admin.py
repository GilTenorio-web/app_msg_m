from django.contrib import admin
from users_manager.models import CustomUser,Room,Message

admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(Message)