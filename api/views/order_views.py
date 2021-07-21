# imports Essential DRF
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# imports Essential MODELS
from api.models import Product, Order, OrderItem, shippingAddress

# imports Essential SERIALIZERS
from api.serializers import ProductSerializer, OrderSerializer

from django.conf import settings

User = settings.AUTH_USER_MODEL
from datetime import datetime


class getMyOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def getMyOrders(request):
#     user = request.user
#     orders = user.order_set.all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


class getOrder(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response(
                {"detail": "Not authorized to view this order"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except:
        return Response(
            {"detail": "Order does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def OrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response({"detail": "Order was paid"}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def OrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response({"detail": "Order was delivered"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addOrderItem(request):
    """
    request.data returns the parsed content of the request body
    """

    user = request.user
    data = request.data

    """
    request.POST # Only handles form data. Only works for 'POST' method.

    request.data # Handles arbitrary data. Works for 'POST', 'PUT' and 'PATCH' methods.
    """
    OrderItem = data["OrderItem"]
    print(OrderItem)

    if OrderItem and len(OrderItem) == 0:
        return Response(
            {"detail": "No Order Items"}, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        # Create order
        order = Order.objects.create(
            user=user,
            shippingPrice=data["shippingPrice"],
            totalPrice=data["totalPrice"],
        )
        # Create shipping address
        shippingAddress = shippingAddress.objects.create(
            order=order,
            address=data["shippingAddress"],
            city=data["city"],
            country=data["country"],
            shippingPrice=data["shippingPrice"],
        )
        # Create order items adn set order to orderItem relationship.

        for items in orderItem:
            product = Product.objects.get(_id=items["product"])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.productTitle,
                qty=items["qty"],
                price=items["price"],
                image=product.image.url,
            )

        # Update stock
        product.countInStock -= item.qty
        product.save()

        subject = "Your Order is Confirmed Email"
        message = f"Hi {request.user.username}, \n\n\n ✅ Your order is confirmed!, Thanks for shoppinng! \n\n Your order {product.title}\n\n\n \n Cheers,\n Dev Team"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)
