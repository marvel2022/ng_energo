from django.db import models
from django.urls import reverse
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save 
from django.core.validators import validate_email
# Create your models here.



import core.models

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название категории: ')
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Категория Slug")
    top  = models.BooleanField(default=False, verbose_name="Top")

    image   = models.ImageField(upload_to='category-image/%d/%m/%Y/', blank=True, null=True, verbose_name='Категория Изображение')
    caption = models.CharField(max_length=300, blank=True, null=True, verbose_name="Подпись к изображению")

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    class Meta:
        ordering=['name',]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category', verbose_name='Kатегория продукта')

    name = models.CharField(max_length=300, unique=True, verbose_name='Название продукта')
    slug = models.SlugField(max_length=360, unique=True, verbose_name='Слаг продукта')
    description   = models.TextField(blank=True, null=True, verbose_name='Описание')
    spesification = models.TextField(blank=True, null=True, verbose_name="Технические характеристики")

    available = models.BooleanField(default=False, verbose_name="Имеется в наличии")
    to_order  = models.BooleanField(default=False, verbose_name="На заказ")

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " | " + self.category.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    class Meta:
        ordering=['category', 'published_at', 'updated_at',]
        verbose_name = 'Товар'
        verbose_name_plural='Продукты'

    @property
    def date(self):
        if self.published_at == self.updated_at:
            return self.published_at
        else:
            return self.updated_at
    @property
    def view_count(self):
        return core.models.ClientView.objects.filter(product=self).count()
    
    # def get_absolute_url(self):
    #     return reverse("core:detail", kwargs={"slug": self.slug})


def new_product_added(sender, instance, created, **kwargs):
    print("this is post_save signal")
    product = instance
    if created:
        subscribers = core.models.Subscriber.objects.all()
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        for sub in subscribers:
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=sub.email,
                    subject="NG ENERGO",
                    html_content=product.name + (" yangi maxsulot qushildi. Kuproq malumot olish uchun quyidagi linkga bosing <a href='https://www.ngenergo.uz/'>NG ENERGO</a>"))
            sg.send(message)

post_save.connect(new_product_added, sender=Product)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', verbose_name='Product Image')
    image   = models.ImageField(upload_to="product-image/%d/%m/%Y/", blank=True, null=True, verbose_name='Image')
    caption = models.CharField(max_length=300, blank=True, null=True, verbose_name="Image Caption")

    def __str__(self):
        return self.product.name + " | " + str(self.pk)
    
    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class HomeImage(models.Model):
    image=models.ImageField(upload_to='home/%d/%m/%Y/', verbose_name="Основное изображение")
    caption = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")

    class Meta:
        verbose_name = 'Основное изображение'
        verbose_name_plural = 'Основные изображения'

    def __str__(self):
        return str(self.pk)
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url



class CertificateImage(models.Model):
    image = models.ImageField(upload_to="certificate/%d/%m/%Y/", verbose_name="Изображение")
    caption = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    possition = models.IntegerField(default=0, verbose_name="Положение")

    class Meta:
        ordering = ['possition']
        verbose_name = 'Сертификаты'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return "ID: " + str(self.pk) + " | " + "Положение: " + str(self.possition)

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class PartnerImage(models.Model):
    image = models.ImageField(upload_to="Partner/%d/%m/%Y/", verbose_name="Изображение")
    caption = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    possition = models.IntegerField(default=0, verbose_name="Положение")

    class Meta:
        ordering = ['possition']
        verbose_name = 'Партнеры'
        verbose_name_plural = 'Партнеры'

    def __str__(self):
        return "ID: " + str(self.pk) + " | " + "Положение: " + str(self.possition)
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
 