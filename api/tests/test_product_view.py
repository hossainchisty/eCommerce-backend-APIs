from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

class ViewTestCase(APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.product_data = {'title': 'test product', 'description': 'test description', 'price': '10.00'}
        self.response = self.client.post(
            reverse('product:product-create'),
            self.product_data,
            format="json",
        )

    def test_api_can_create_a_product(self):
        """Test the api has product creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


    # def test_api_can_get_a_product(self):
    #     """Test the api can get a given product."""
    #     product = Product.objects.get()
    #     response = self.client.get(
    #         reverse('details',
    #         kwargs={'pk': product.id}), format="json")

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertContains(response, bucketlist)

    # def test_api_can_update_product(self):
    #     """Test the api can update a given product."""
    #     change_bucketlist = {'titile': 'Something new'}
    #     res = self.client.put(
    #         reverse('details', kwargs={'pk': bucketlist.id}),
    #         change_bucketlist, format='json'
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_api_can_delete_product(self):
    #     """Test the api can delete a product."""
    #     product = Product.objects.get()
    #     response = self.client.delete(
    #         reverse('details', kwargs={'pk': product.id}),
    #         format='json',
    #         follow=True)

    #     self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)