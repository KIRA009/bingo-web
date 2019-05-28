from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(Game)
admin.site.register(FriendRequest)
admin.site.register(Invite)
admin.site.register(Records)
admin.site.register(Friends)