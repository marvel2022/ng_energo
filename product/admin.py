from django.contrib import admin
from django.db.models import TextField
from tinymce.widgets import TinyMCE

# Register your models here.


from .models import (
    Category,
    Product,
    Image,
    HomeImage,
    CertificateImage,
    PartnerImage,
)


class CategoryAdmin(admin.ModelAdmin):
    # ('name', 'slug', 'image', 'caption', 'date_added', )
    list_display=('name', 'slug', 'top')
    list_display_links=('name',)
    search_fields=('name', 'slug',)
    ordering=('name', 'slug', 'top')
    list_editable = ('slug', 'top')

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ("Category", {
            "fields": (
                'name', 'slug', 'top', 'image', 'caption', 
            ),
        }),
    )

admin.site.register(Category, CategoryAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    max_num = 3

class ProductAdmin(admin.ModelAdmin):
    # ('category', 'name', 'slug', 'description', 'spesification', 'published_at', 'updated_at', )
    inlines = [ImageInline,]

    list_display=('category', 'name', 'slug', "available", "to_order", 'published_at', 'updated_at',)
    list_display_links=('name', 'published_at', 'updated_at',)
    ordering=('category', 'name', 'slug', "available", "to_order", 'published_at', 'updated_at',)
    list_editable=('category', 'slug', "available", "to_order",)
    serach_fields=('category', 'name', 'slug', "available", "to_order", 'published_at', 'updated_at',)

    prepopulated_fields = {'slug': ('name',)}

    fieldsets=(
        ('Product', {
            'fields':(
                'category', 'name', 'slug', "available", "to_order",
            )
        }),
        ('Desc/Spec', {
            'fields': (
                 'description', 'spesification',
            )
        }),
    )

    formfield_overrides = {
        TextField: {'widget': TinyMCE }
    }

admin.site.register(Product, ProductAdmin)

admin.site.register(HomeImage)
admin.site.register(CertificateImage)
admin.site.register(PartnerImage)
