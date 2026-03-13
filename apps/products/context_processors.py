from .models import Category

def category_context(request):
    return {
        'all_main_categories' : Category.objects.filter(parent=None, show_in_navbar=True )
    }