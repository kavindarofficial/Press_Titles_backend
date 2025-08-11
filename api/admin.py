from django.contrib import admin

# Register your models here.
from .models import NewspaperTitle
@admin.register(NewspaperTitle)
class NewspaperTitleAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the 'name' field in the list view
    search_fields = ('name',)  # Add search functionality to search by name