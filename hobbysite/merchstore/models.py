from django.db import models
from django.urls import reverse

# Create your models here.

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    #to have product types in ascending order i think ???
    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    #idk abt the max digits ??
    price = models.DecimalField(decimal_places=2, max_digits=10)
    producttype = models.ForeignKey(ProductType,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name= "type")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('ledger:merchstore-item', args=[self.pk])
    
    class Meta:
        ordering = ['name']


            

