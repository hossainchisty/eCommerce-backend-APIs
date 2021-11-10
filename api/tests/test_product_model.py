from django.test import TestCase
from api.models import Product
from rest_framework import status


class ProductTest(TestCase):
    """Test suite for the product model."""

    def setUp(self):
        """Set up the for Product model"""
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

    def test_product_has_been_created_two_times(self):
        """Test the product has been created to two times."""
        products = Product.objects.all()
        self.assertEqual(len(products), 2)

    def test_product_string_representation(self):
        """Test product string representation."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(str(product), "Test Product 1")

    def test_product_title(self):
        """Test the title of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.title, "Test Product 1")

    def test_product_price(self):
        """Test the price of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.price, 10)
    
    def test_product_price_is_not_expected(self):
        """Test the price of the product is not expected."""
        product = Product.objects.get(title="Test Product 1")
        self.assertNotEquals(product.price, 100)
    
    def test_product_price_is_not_negative(self):
        """Test the price of the product is not negative."""
        product = Product.objects.get(title="Test Product 1")
        self.assertNotEquals(product.price, -10)


    def test_product_rating(self):
        """Test the rating of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.rating, 5)
    
    def test_product_rating_is_negative(self):
        """Test the rating of the product is negative."""
        product = Product.objects.get(title="Test Product 1")
        self.assertNotEquals(product.rating, -5.00)
        

    def test_product_reviews(self):
        """Test the number of reviews of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.numbersOfReview, 1)

    def test_product_review_is_negative(self):
        """Test the review of the product is negative."""
        product = Product.objects.get(title="Test Product 1")
        self.assertNotEquals(product.numbersOfReview, -1)

    def test_product_count_in_stock(self):
        """Test the count in stock of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.countInStock, 100)
    
    def test_product_is_out_of_stock(self):
        """Test the product is out of stock."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.isOutOfStock, False)
    
    def test_product_is_available(self):
        """Test the product is available."""
        product = Product.objects.get(title="Test Product 1")
        self.assertTrue(product.isAvailable)

    def test_product_brand(self):
        """Test the brand of the product."""
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.brand, "Test Brand 1")
