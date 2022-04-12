from django.db import models
from django.urls import reverse
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save 
from django.core.validators import validate_email

from product.models import (
    Category,
    Product,
    Image,
    HomeImage,
)

# Create your models here.


class ClientView(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_view', verbose_name='Product')
    client_ip = models.GenericIPAddressField(default='0.0.0.0')

    def __str__(self):
        return str(self.client_ip)
    
    class Meta:
        verbose_name_plural='Просмотры клиентов'


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    # conf_num = models.CharField(max_length=15, default=00000000)
    # confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчик'

    def __str__(self):
        # return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"
        return self.email


class ClientContact(models.Model):
    fullname = models.CharField(max_length=50, default='client name', blank=True, null=True, verbose_name="Имя клиента")
    contactinfo = models.CharField(max_length=70, blank=True, null=True, verbose_name="Контактная информация")
    message = models.TextField(blank=True, null=True, verbose_name="Сообщение")
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['added_date']
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return self.fullname + self.contactinfo

def new_contact_added(sender, instance, created, **kwargs):
    print("this is post_save signal")
    contact = instance
    if created:
        
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        try:
            validate_email(contact.contactinfo)
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails='neftgazenergo@mail.ru',
                    # to_emails='dovurovjamshid95@gmail.com',
                    subject="NG ENERGO",
                    html_content=(f"Ismi: {contact.fullname}<br>Email: <a href=\'mailto:{contact.contactinfo}\'>{contact.contactinfo}</a> <br><b>Xabar:</b> <br><br>{contact.message}"))
            sg.send(message)
        except:
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails='neftgazenergo@mail.ru',
                    # to_emails='dovurovjamshid95@gmail.com',
                    subject="NG ENERGO",
                    html_content=(f"Ismi: {contact.fullname}<br>Tel: <a href=\'tel:{contact.contactinfo}\'>{contact.contactinfo}</a> <br><b>Xabar:</b> <br><br>{contact.message}"))
            sg.send(message)

post_save.connect(new_contact_added, sender=ClientContact)