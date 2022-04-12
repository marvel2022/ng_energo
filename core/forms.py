from tinymce.widgets import TinyMCE
from django import forms

from product.models import (
    Product,
    Category,
    Image,
    HomeImage,
)
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = '__all__'

class ProductForm(forms.ModelForm):
    # ('category', 'name', 'slug', 'description', 'spesification', 'available', 'published_at', 'updated_at', )
    category = forms.Select(attrs={'class' : 'blog-category'},)
    
    name = forms.CharField( max_length=300, label="Имя")
    slug = forms.CharField( max_length=360, label="Слизняк")
    description = forms.CharField(widget=TinyMCE)

    spesification = forms.CharField(widget=TinyMCE)
    available = forms.BooleanField( label="Имеется в наличии")
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'spesification', 'available',]

        widgets = {
            'tag'  : forms.Select(attrs={'class' : 'blog-category'}),
        }


class ProductImagesForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="Образ")
    caption = forms.CharField(max_length=300, required=False, label='Заголовок')
    class Meta:
        model = Image
        fields=['image', 'caption']


class HomeIMageForm(forms.ModelForm):
    class Meta:
        model = HomeImage

        fields = '__all__'
