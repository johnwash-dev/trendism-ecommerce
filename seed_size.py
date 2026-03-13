import os
import django
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Identify the dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings') 
django.setup()

try:
    from apps.products.models import Category, Size 
except ImportError as e:
    logger.error(f"Import Error: {e}. Check if 'apps.products' is the correct path.")
    sys.exit(1)

def seed_category_sizes():
    # Size definitions
    top_wear_sizes = ['S', 'M', 'L', 'XL', 'XXL']
    bottom_wear_sizes = ['28', '30', '32', '34', '36', '38']
    shoe_sizes = ['6', '7', '8', '9', '10']
    ethnic_wear_sizes = ['36', '38', '40', '42', '44']
    kids_wear_sizes = ['2-3Y', '4-5Y', '6-7Y', '8-9Y', '10-11Y', '12-13Y']

    categories = Category.objects.all()

    if not categories.exists():
        logger.warning("No categories found in the database. Please add categories first.")
        return

    for cat in categories:
        name = cat.name.lower()
        target_sizes = []

        # Logic for categorization
        if any(kw in name for kw in ['kids', 'boy', 'girl']):
            target_sizes = kids_wear_sizes
        elif any(kw in name for kw in ['kurti', 'kurta', 'ethnic', 'set']):
            target_sizes = ethnic_wear_sizes
        elif any(kw in name for kw in ['vest', 'undershirt', 'bra']):
            target_sizes = top_wear_sizes
        elif any(kw in name for kw in ['brief', 'trunk', 'boxer', 'panty', 'innerwear']):
            target_sizes = bottom_wear_sizes
        elif any(kw in name for kw in ['shirt', 't-shirt', 'top', 'sweater', 'sweatshirt', 'western', 'hoodies']):
            target_sizes = top_wear_sizes
        elif any(kw in name for kw in ['pant', 'jean', 'trouser', 'short', 'legging', 'jegging', 'lower']):
            target_sizes = bottom_wear_sizes
        elif any(kw in name for kw in ['shoe', 'slipper', 'footwear']):
            target_sizes = shoe_sizes

        # Database transaction using get_or_create
        for s_name in target_sizes:
            obj, created = Size.objects.get_or_create(category=cat, name=s_name)
            if created:
                logger.info(f"Added size '{s_name}' to category '{cat.name}'")
            else:
                logger.debug(f"Size '{s_name}' already exists for '{cat.name}'")

if __name__ == "__main__":
    logger.info("Starting professional size seeding process...")
    try:
        seed_category_sizes()
        logger.info("Seeding process completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during seeding: {e}")
