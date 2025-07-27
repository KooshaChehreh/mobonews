import unittest
from unittest.mock import patch, MagicMock
from lxml import html
from scraper.scrapers.ilandino import ScrapIlandino
from scraper.models import Product

class TestScrapIlandino(unittest.TestCase):
    def setUp(self):
        self.scraper = ScrapIlandino()
        self.sample_url = "https://dizoland.com/product/roborock-saros-10r/"
        self.sample_product_name = "Roborock Saros 10R"
        self.sample_html = """
        <html>
          <body>
            <div class="product">
              <div class="summary">
                <h1>جارو رباتیک Roborock Saros 10R</h1>
                <p><span class="price"><bdi>171,000,000</bdi></span></p>
                <ul>
                  <li>قدرت مکش: 22,000 پاسکال</li>
                  <li>سیستم ناوبری: StarSight Autonomous System 2.0</li>
                  <li>گوشه زنی دقیق</li>
                </ul>
                <form class="variations_form" data-product_variations='[{"attributes":{"attribute_pa_color":"black"},"display_price":171000000},{"attributes":{"attribute_pa_color":"white"},"display_price":180000000}]'>
                </form>
              </div>
            </div>
          </body>
        </html>
        """
        self.sample_product = MagicMock()
        self.sample_product.url = self.sample_url
        self.sample_product.product_name = self.sample_product_name
        self.sample_product.product_type = Product.PRODUCT_TYPE_PHONE

    @patch('scraper.scrapers.base_scraper.Scraper.get_scrap_urls')
    @patch('scraper.models.Product.objects')
    @patch('requests.get')
    def test_scrap_single_product_success(self, mock_requests_get, mock_product_objects, mock_get_urls):
        mock_get_urls.return_value = [self.sample_url]
        mock_product_objects.get.return_value = self.sample_product
        mock_response = MagicMock(content=self.sample_html.encode())
        mock_requests_get.return_value = mock_response
        with patch('scraper.models.Product.save_product_data', return_value=f"Updated {self.sample_product_name}") as mock_save:
            results = self.scraper.scrap(product=self.sample_product_name)
        self.assertEqual(results, None)
        mock_save.assert_called_once_with(
            product_name=self.sample_product_name,
            color_price_data={"black": 171000000, "white": 180000000},
            description="",
            price=None
        )

    @patch('scraper.scrapers.base_scraper.Scraper.get_scrap_urls')
    @patch('scraper.models.Product.objects')
    def test_scrap_single_product_not_found(self, mock_product_objects, mock_get_urls):
        mock_get_urls.return_value = [self.sample_url]
        mock_product_objects.get.side_effect = Product.DoesNotExist
        results = self.scraper.scrap(product="non-existent")
        self.assertEqual(results, None)

    @patch('scraper.scrapers.base_scraper.Scraper.get_scrap_urls')
    @patch('scraper.models.Product.objects')
    @patch('requests.get')
    def test_scrap_all_products(self, mock_requests_get, mock_product_objects, mock_get_urls):
        mock_get_urls.return_value = [self.sample_url]
        mock_product_objects.get.return_value = self.sample_product
        mock_response = MagicMock(content=self.sample_html.encode())
        mock_requests_get.return_value = mock_response
        with patch('scraper.models.Product.save_product_data', return_value=f"Updated {self.sample_product_name}") as mock_save:
            results = self.scraper.scrap()
        self.assertEqual(results, None)
        mock_save.assert_called_once()

    def test_extract_color_price_valid(self):
        form_node = html.fromstring(self.sample_html).xpath('//form[contains(@class, "variations_form")]')[0]
        result = self.scraper.extract_color_price([form_node])
        self.assertEqual(result, {"black": 171000000, "white": 180000000})

    def test_extract_color_price_invalid_json(self):
        invalid_html = '<form class="variations_form" data-product_variations="[invalid_json]"></form>'
        form_node = html.fromstring(invalid_html).xpath('//form[contains(@class, "variations_form")]')[0]
        result = self.scraper.extract_color_price([form_node])
        self.assertEqual(result, {})
