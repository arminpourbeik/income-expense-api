from django.contrib import admin

from expenses import models

admin.site.register(models.Expense)
