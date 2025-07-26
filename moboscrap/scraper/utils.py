from .models import Product

def save_product_data(phone_model, color_price_data, description, warranty, stock):
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
        # Check if record exists
        if not Product.objects.filter(phone_model=phone_model).exists():
            return f"No record found for {phone_model}"
        
        # Update existing record
        Product.objects.filter(phone_model=phone_model).update(
            color_prices=color_price_data or {},
            description=description or '',
            warranty=warranty or '',
            stock=stock or 0
        )
        return f"Updated {phone_model}"
    except Exception as e:
        return f"Error updating {phone_model}: {e}"
   