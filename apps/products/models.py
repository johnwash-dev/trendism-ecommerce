import os
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.
def get_product_image_url(instance, filename):
    category_name = slugify(instance.category.name)
    return os.path.join('products', category_name, filename)

def get_thumbnail_path(instance, filename):
    category_name = slugify(instance.category.name)
    return os.path.join('products', category_name, 'thumbnails', filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/icons/', null=True, blank=True, storage=MediaCloudinaryStorage())
    is_trending = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Home page trending categories order")
    nav_order = models.PositiveIntegerField(default=0, help_text="Navbar mega menu order")
    show_in_navbar = models.BooleanField(default=True, help_text="specific categories showing in navbar")

    class Meta:
        ordering = ['nav_order','order']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

class Color(models.Model):
    color_name = models.CharField(max_length=50)
    code = models.CharField(max_length=7, help_text="HEX code, e.g.,#ffff")

    def __str__(self):
        return self.color_name
    
    
class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    style_group = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text="give me the same group name to same design products for identify the color variation (e.g., 'slim-fit-cotton-shirt-01')"
    )
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.IntegerField(default=0, editable=False)

    thumbnail = models.ImageField(upload_to=get_thumbnail_path, storage=MediaCloudinaryStorage())

    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def get_discount_percent(self):
        if self.discount_price and self.discount_price > 0:
            discount = ((self.original_price - self.discount_price) / self.original_price) * 100
            return int(discount) 
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.name}")
        

        if self.original_price > 0 and self.discount_price:
            offer = self.original_price - self.discount_price
            percentage = (offer/ self.original_price) * 100
            self.discount_percentage = round(percentage)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} - {self.name}"
    
class Size(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sizes')
    name = models.CharField(max_length=20, default=0)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.size.name}'
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='products/gallery/', storage=MediaCloudinaryStorage())

class HomeBanners(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/', storage=MediaCloudinaryStorage())
    link = models.CharField(max_length=500, help_text="Example: /category/men-shirts/")
    is_active = models.BooleanField(default=True, help_text="check this to show the banner on home page")

    def __str__(self):
        return self.title
    