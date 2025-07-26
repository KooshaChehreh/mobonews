class ProductNotFound(Exception):

    def __init__(self, product_name=None):
        self.message = f"No product record found for the specified model {product_name}."
        self.code = "product_not_found"
        super().__init__(self.message)