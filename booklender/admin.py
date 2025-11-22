from django.contrib import admin

from booklender.models import userData,borrowerDetails,AddBook,ReviewList
# Register your models here.


admin.site.register(userData)
admin.site.register(borrowerDetails)
admin.site.register(AddBook)
admin.site.register(ReviewList)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'modified_at')
    search_fields = ('title', 'author')
