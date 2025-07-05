from django.db import models
from django.contrib.auth.models import User  

class Wishlist(models.Model):
     name = models.CharField(max_length=100)
     description = models.TextField(blank=True)
     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists", null=True, blank=True)
     contributors = models.ManyToManyField(User, related_name="shared_wishlists", blank=True)  # For invite/mocking
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     def __str__(self):
        return self.name

class Product(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    name = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_products", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
