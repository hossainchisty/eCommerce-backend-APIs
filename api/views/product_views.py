# imports Essential DRF
from taggit.models import Tag
from rest_framework import status
from django.db.models import Count
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from taggit.serializers import TagListSerializerField, TaggitSerializer

# imports Essential MODELS
from api.models import Product, Review

# imports Essential SERIALIZERS
from api.serializers import ProductSerializer

from api.pagination import ProductPagination
from django.conf import settings

User = settings.AUTH_USER_MODEL


class getProductList(generics.ListAPIView):
    """
    ✅Get all products List
        ♻ Method: GET
    """

    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "rating"]


class CreateProduct(generics.CreateAPIView):
    """
    ✅Create new product in store.
        ♻ Method: POST
    """

    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UpdateProduct(generics.UpdateAPIView):
    """
    ✅Update product wtih given id.
        ♻ Method: PUT
    """

    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DeleteProduct(generics.DestroyAPIView):
    """
    ✅Delete product wtih given id.
        ♻ Method: DELETE
    """

    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getProduct(request, pk):
    """
    ✅Retrieve product by ID.
    """
    try:
        product = Product.objects.get(_id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    except Product.DoesNotExist:
        message = {"detail": "Sorry! This product is no longer available"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getTopProduct(request):
    """
    ✅Retrieve top rated products.
    """

    products = Product.objects.filter(rating__gte=4).order_by("-rating")[0:5]

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getSimilarProduct(request):
    """
    ✅Retrieving products by similarity
    """
    products = Product.objects.filter(rating__gte=4).order_by("-rating")[0:5]
    product_tags_ids = Product.tags.values_list("id", flat=True)
    print(product_tags_ids)
    products = Product.objects.filter(tags__in=product_tags_ids).exclude(
        _id=product_tags_ids[0]
    )
    print(products)

    similar_products = products.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-created"
    )[:4]

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # Review already exists
    reviewAlreadyExists = product.review_set.filter(user=user).exists()
    if reviewAlreadyExists:
        content = {"detail": "Product already reviewed, Thanks"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif data["rating"] == 0:
        content = {"detail": "Please select a rating..."}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Create review
    else:
        createReviews = Review.objects.create(
            user=user,
            product=product,
            fullName=user.first_name,
            rating=data["rating"],
            feedback=data["feedback"],
            riderReview=data["riderReview"],
        )

        review = Product.review_set.all()
        product.numbersOfReview = len(review)

        total = 0
        for i in review:
            total += i.rating

        product.rating = total / len(review)
        product.save()

        return Response("Review Added, Thanks!")


# python3 manage.py check --deploy
