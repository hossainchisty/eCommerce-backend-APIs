from django.test import TestCase
from api.models import Product


class ProductTest(TestCase):
    def setUp(self):
        """Test module for Product model"""
        Product.objects.create(
            title="Test Product 1",
            price=10,
            rating=5,
            numbersOfReview=1,
            countInStock=100,
            brand="Test Brand 1",
        )
        Product.objects.create(title="Test Product 2", price=190, brand="Test Brand 2")

    def tearDown(self):
        """Tear down the test case."""
        Product.objects.all().delete()

    def test_product_title(self):
        """Test the title of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.title, "Test Product 1")

    def test_product_price(self):
        """Test the price of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.price, 10)

    def test_product_rating(self):
        """Test the rating of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.rating, 5)

    def test_product_reviews(self):
        """Test the number of reviews of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.numbersOfReview, 1)

    def test_product_count_in_stock(self):
        """Test the count in stock of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.countInStock, 100)

    def test_product_brand(self):
        """Test the brand of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.brand, "Test Brand 1")
