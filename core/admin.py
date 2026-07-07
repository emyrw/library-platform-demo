from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Loan


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'role']
    list_filter = ['role']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'media_type']
    search_fields = ['title', 'author', 'publisher', 'media_type']
    list_filter = ['media_type']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader','due_date']
    search_fields = ['book__title', 'reader__username']
