from django.contrib import admin

from .models import *


# Register your models here.


class BookAdmin(admin.ModelAdmin):
    # fieldsets = []
    list_display = ['name', 'author']
    list_filter = ['author']
    search_fields = ['name', 'author', 'user__username']
    list_per_page = 50
    pass


class ShelfAdmin(admin.ModelAdmin):
    # fieldsets = []
    list_display = ['number', 'library']
    list_filter = ['library__name']
    search_fields = ['books__name', 'library__name']
    list_per_page = 20
    pass


class LibraryAdmin(admin.ModelAdmin):
    # fieldsets = []
    list_display = ['name', 'address']
    list_filter = ['city']
    search_fields = ['city', 'books__name', 'name']
    list_per_page = 10
    pass


class ShelfDetailAdmin(admin.ModelAdmin):
    # fieldsets = []
    list_display = ['library_name', 'shelf', 'book', 'number']
    list_filter = ['shelf__library__name']
    search_fields = ['book__name']
    list_per_page = 100
    pass


class LibraryDetailAdmin(admin.ModelAdmin):
    # fieldsets = []
    list_display = ['library', 'book']
    list_filter = ['library__name']
    search_fields = ['book__name', 'library__name']
    list_per_page = 100
    pass


class BorrowAdmin(admin.ModelAdmin):
    # fieldsets = []
    list_display = ['library', 'shelf', 'book', 'user_name', 'get_date', 'return_date']
    list_filter = ['get_date', 'return_date', 'library__name']
    search_fields = ['book__name', 'user__username', 'library__name']
    list_per_page = 100
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Shelf, ShelfAdmin)
admin.site.register(ShelfDetail, ShelfDetailAdmin)
admin.site.register(LibraryDetail, LibraryDetailAdmin)
admin.site.register(Borrow, BorrowAdmin)
