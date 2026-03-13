from django.contrib import admin
from .models import Product, ProductImage, Category, Variations, HomeBanners,Size,Color


# Register your models here.



@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['category', 'name']
    list_filter = ['category']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class VariationInline(admin.TabularInline):
    model = Variations
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            object_id = request.resolver_match.kwargs.get('object_id')
            
            if object_id:
                try:
                    product = Product.objects.get(pk=object_id)
                    kwargs["queryset"] = Size.objects.filter(category=product.category)
                except Product.DoesNotExist:
                    kwargs["queryset"] = Size.objects.none()
            else:
                kwargs["queryset"] = Size.objects.none() 
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'color', 'style_group', 'original_price', 'seller', 'discount_price', 'category', 'is_featured']
    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter), 
        'is_featured', 
        'brand'
    )
    list_editable = ['is_featured', 'discount_price']
    search_fields = ['name', 'brand']
    prepopulated_fields = {'slug': ('brand','name',)}
    autocomplete_fields = ['color','category']



    inlines = [ProductImageInline, VariationInline]

    def save_model(self, request, obj, form, change):
        if not obj.seller:
            obj.seller = request.user
        super().save_model(request, obj, form, change)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'code']
    search_fields = ['color_name']

@admin.register(HomeBanners)
class HomeBannersAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'link']
    list_editable = ['is_active']