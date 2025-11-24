from django.contrib import admin
from .models import User, Book, BookRequest, IssuedBook

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'total_copies', 'available_copies')
    search_fields = ('title', 'author')

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'status', 'request_date', 'approved_by')
    list_filter = ('status', 'request_date')
    search_fields = ('student__username', 'book__title')

@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issue_date', 'return_date')
    list_filter = ('issue_date', 'return_date')
    search_fields = ('student__username', 'book__title')
