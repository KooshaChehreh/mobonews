from .models import Product

def save_product_data(phone_model, color_price_data, description=None, warranty=None, stock=None):
    """
    Save or update a product record with color-price JSON, description, warranty and stock.
    
    Args:
        phone_model (str): Name of the product (e.g., "Samsung Galaxy S24 FE")
        color_price_data (dict): JSON data like {"black-phantom": 135000000, ...}
        description (str): Product description text
        warranty (str): Warranty name if it is available on site
        stock (int): The invetory of the product
    """
    try:
        if not Product.objects.filter(phone_model=phone_model).exists():
            return f"No record found for {phone_model}"
        
        Product.objects.filter(phone_model=phone_model).update(
            color_prices=color_price_data or {},
            description=description,
            warranty=warranty,
            stock=stock
        )
        return f"Updated {phone_model}"
    except Exception as e:
        return f"Error updating {phone_model}: {e}"
   