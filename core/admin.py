from django.contrib import admin
from django.db.models import TextField
from tinymce.widgets import TinyMCE

# Register your models here.


from .models import (
    ClientView,
    Subscriber,
    ClientContact,
)

admin.site.register(ClientView)
admin.site.register(Subscriber)
admin.site.register(ClientContact)