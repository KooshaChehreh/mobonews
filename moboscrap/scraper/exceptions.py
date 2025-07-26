class ProductNotFound(Exception):

    def __init__(self, phone_model=None):
        self.message = f"No product record found for the specified model {phone_model}."
        self.code = "product_not_found"
        super().__init__(self.message)