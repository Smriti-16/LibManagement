from django.contrib import admin
from .models import Add_Book as AddBook
from .models import Issued

# Register your models here
admin.site.register(AddBook)


admin.site.register(Issued)


