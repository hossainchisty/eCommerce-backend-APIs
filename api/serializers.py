# imports Essential DRF & Simple JWT
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# imports Essential MODELS
from .models import Product, Review, Order, OrderItem, shippingAddress, CustomUser
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(required=True)
    name = serializers.SerializerMethodField(read_only=True)
    # isAdmin = serializers.SerializerMethodField(read_only=True)
    # is_active = serializers.SerializerMethodField(read_only=True)
    # days_since_joined = serializers.SerializerMethodField()
    # # birthday = serializers.SerializerMethodField()
    # # gender = serializers.SerializerMethodField()
    # country = serializers.SerializerMethodField()
    # mobile_phone = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "_id",
            "email",
            "name",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get__id(self, obj):
        return obj.id

    def get_name(self, obj):
        name = obj.first_name + " " + obj.last_name
        if name == "":
            name = obj.email
        return name

    def get_is_active(self, obj):
        return obj.is_active

    def get_isAdmin(self, obj):
        return obj.is_superuser

    def get_days_since_joined(self, obj):
        """
        Note: You need to include USE_TZ=True in settings to get an aware datetime
        """
        return (timezone.now() - obj.date_joined).days


class UserSerializerWithToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, token):
        token = super(UserSerializerWithToken, cls).get_token(user)
        return token


class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    def get_tags(self, obj):
        tags = obj.tags_set.all()
        serializer = TaggitSerializer(tags, many=True)
        return serializer.data


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class shippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = shippingAddress
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
