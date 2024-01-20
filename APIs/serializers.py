from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Customer, StoreOwner,ProductMarket,Product,Wholesaler

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user', 'number', 'points')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

class WholesellerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Wholesaler
        fields = ('id', 'user', 'number', 'points')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        wholeseller = Wholesaler.objects.create(user=user, **validated_data)
        return wholeseller

class StoreOwnerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StoreOwner
        fields = ('id', 'user', 'number', 'points')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        store_owner = StoreOwner.objects.create(user=user, **validated_data)
        return store_owner
class AuthorizationSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_type = serializers.CharField()
    user_data = serializers.SerializerMethodField()

    def get_user_data(self, obj):
        user_type = obj['user_type']

        if user_type == 'customer':
            return CustomerRegistrationSerializer(obj['user_data']).data
        elif user_type == 'store_owner':
            return StoreOwnerRegistrationSerializer(obj['user_data']).data
        else:
            return None

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user', 'number', 'points')
class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreOwner
        fields = ('id', 'user', 'number', 'points')



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'barcode', 'name', 'qrcode', 'is_redeemed', 'got_the_tokens')

class ProductMarketSerializer(serializers.ModelSerializer):
    qr_code = serializers.SerializerMethodField(source='product.qrcode')  # Use SerializerMethodField

    class Meta:
        model = ProductMarket
        fields = ('id', 'name', 'image', 'point_to_redeem', 'product', 'redeemed_time', 'redeemed_at', 'qr_code')

    def get_qr_code(self, obj):
        return obj.product.qrcode.url  # Assuming qrcode is an ImageField, adjust as needed
