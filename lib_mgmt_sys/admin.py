from django.contrib import admin
from lib_mgmt_sys.models import Books, Author,AuthorPenName, Students

# Register your models here.
admin.site.register(Books)
admin.site.register(Author)
admin.site.register(AuthorPenName)
admin.site.register(Students)

