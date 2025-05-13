from django.db import models
from django.urls import reverse
from user_management.models import Profile
from django.core.validators import MinValueValidator

PRODUCT_STATUS = (
    ('AVL', 'Available'),
    ('SALE', 'On Sale'),
    ('OOS', 'Out of Stock'),
)

TRANSACTION_STATUS = (
    ('CART', 'On Cart'),
    ('PAY', 'To Pay'),
    ('SHIP', 'To Ship'),
    ('RECEIVE', 'To Receive'),
    ('DELIVERED', 'Delivered'),
)


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    producttype = models.ForeignKey(ProductType,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name="type")
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE, null=True,
                              related_name='products')
    stock = models.PositiveIntegerField()
    status = models.CharField(max_length=15,
                              choices=PRODUCT_STATUS,
                              default="AVL")
    merch_image = models.ImageField(
        upload_to='merchstore/',
        null=True,
        blank=True,
    )
    sale_percent = models.PositiveIntegerField(validators= [MinValueValidator(1)], null=True, blank=True)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:merchstore-item', args=[self.pk])

    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    buyer = models.ForeignKey(Profile,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='transactions')
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='transacted')
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=TRANSACTION_STATUS)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer}: {self.product}"
