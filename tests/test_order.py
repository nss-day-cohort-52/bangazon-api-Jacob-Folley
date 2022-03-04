from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product, PaymentType, OrderProduct


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        # CREATE A PAYMENT TYPE ?
        self.payment_type1 = PaymentType.objects.create(
            merchant_name = 'visa',
            acct_number = 1234567891234567,
            customer=self.user1
        )

        self.user2 = User.objects.filter(store=None).last()
        self.product = Product.objects.get(pk=1)

        # self.order1 = Order.objects.create(
        #     user=self.user1
        # )

        # self.order1.products.add(product)

        # self.order2 = Order.objects.create(
        #     user=self.user2
        # )

        # self.order2.products.add(product)


        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

    # def test_list_orders(self):
    #     """The orders list should return a list of orders for the logged in user"""
    #     response = self.client.get('/api/orders')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertEqual(len(response.data), 1)

    # def test_delete_order(self):
    #     response = self.client.delete(f'/api/orders/{self.order1.id}')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # TODO: Complete Order test
    def test_payment_order(self):
        """
        Ensure we acn complete order by adding a payment type.
        """
        orderObject = self.client.get('/api/orders/current')
        orderObject.data["payment_type"] = self.payment_type1.id
       
        # Initiate PUT request and capture the response
        response = self.client.put(f'/api/orders/{orderObject.data["id"]}/complete', orderObject.data, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        responseOrder = Order.objects.get(pk=orderObject.data['id'])
        print(responseOrder.payment_type)
    
        self.assertEqual(responseOrder.payment_type, self.payment_type1)

    def test_product_cart(self):
        """
        Ensure adding a product to the cart adds it to open order.
        """
        productObject = self.client.get('/api/products/1')
       
        # Initiate PUT request and capture the response
        response = self.client.post(f'/api/products/{productObject.data["id"]}/add_to_order')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # Initiate GET request and capture the response
        # responseOrder = OrderProduct.objects.get(pk=productObject.data['id'])
    


        

