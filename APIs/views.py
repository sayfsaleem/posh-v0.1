from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerRegistrationSerializer, StoreOwnerRegistrationSerializer,CustomerSerializer,ShopOwnerSerializer,WholesellerRegistrationSerializer,ProductSerializer
from main.models import Customer,StoreOwner,Wholesaler,Product
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
class CustomerRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreOwnerRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StoreOwnerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WholeSellerRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = WholesellerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from main.models import Customer, StoreOwner
from django.core.exceptions import ObjectDoesNotExist


class AuthorizationView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)

            try:
                customer = Customer.objects.get(user=user)
                user_type = 'Customer'
                user_data = CustomerSerializer(customer).data
            except ObjectDoesNotExist:
                try:
                    store_owner = StoreOwner.objects.get(user=user)
                    user_type = 'StoreOwner'
                    user_data = ShopOwnerSerializer(store_owner).data
                except ObjectDoesNotExist:
                    return Response({'error': 'User type not recognized'}, status=status.HTTP_400_BAD_REQUEST)

            response_data = {
                'token': token.key,
                'user_type': user_type,
                'user_data': user_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



from rest_framework import generics
from main.models import ProductMarket
from .serializers import ProductMarketSerializer

class ProductMarketListView(generics.ListAPIView):
    queryset = ProductMarket.objects.all()
    serializer_class = ProductMarketSerializer

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class MarkTokensView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        barcode = request.data.get('barcode', None)

        if barcode:
            try:
                product = Product.objects.get(barcode=barcode)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the product has already been scanned
            if product.got_the_tokens:
                return Response({'error': 'Product already scanned'}, status=status.HTTP_400_BAD_REQUEST)

            # Mark 'got_the_tokens' as True
            product.got_the_tokens = True
            product.save()

            # Add 10 points to the user's account
            user = request.user
            profile_models = [Customer, Wholesaler, StoreOwner]  # Add more models if needed

            for model in profile_models:
                try:
                    profile = model.objects.get(user=user)
                except model.DoesNotExist:
                    continue

                points_to_add = 10
                profile.points += points_to_add
                profile.save()

            # Optionally, you can include the added points in the response
            product.points_added = True

            # Serialize the updated product data
            product_serializer = ProductSerializer(product)

            response_data = {
                'product': product_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'error': 'Barcode not provided'}, status=status.HTTP_400_BAD_REQUEST)
from django.http import JsonResponse
import json
@csrf_exempt
def get_datas(request):
    if request.method == 'POST':
        authorization_header = request.headers.get('Authorization')
        print(authorization_header)
        # Use request.body to get the raw request body
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        word = body.get('qrcode')  # Assuming 'data' is the key you are sending from React Native
        print(word)

        # Add your logic for processing the barcode data here

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Data received successfully'},status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserDataView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            customer = Customer.objects.get(user=user)
            user_type = 'Customer'
            user_data = CustomerSerializer(customer).data
        except ObjectDoesNotExist:
            try:
                store_owner = StoreOwner.objects.get(user=user)
                user_type = 'StoreOwner'
                user_data = ShopOwnerSerializer(store_owner).data
            except ObjectDoesNotExist:
                return Response({'error': 'User type not recognized'}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'token': str(request.auth),
            'user_type': user_type,
            'user_data': user_data
        }

        return Response(response_data, status=status.HTTP_200_OK)


from datetime import datetime

class MarkProductRedeemedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Check if the user is associated with the Customer model
        try:
            customer = Customer.objects.get(user=user)
            return Response({'error': 'Customers are not allowed to redeem products'}, status=status.HTTP_403_FORBIDDEN)
        except Customer.DoesNotExist:
            pass  # The user is not a customer, proceed with redemption

        barcode = request.data.get('barcode')

        if not barcode:
            return Response({'error': 'Barcode not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(barcode=barcode)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if product.is_redeemed:
            return Response({'error': 'Product already redeemed'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the product as redeemed
        product.is_redeemed = True
        product.save()

        # Update ProductMarket fields
        try:
            product_market = ProductMarket.objects.get(product=product)
            product_market.redeemed_at = datetime.now().date()  # Set redeemed_at to the current date
            product_market.redeemed_time = datetime.now().time()  # Set redeemed_time to the current time
            product_market.save()
        except ProductMarket.DoesNotExist:
            return Response({"error": "Product isn't in the market"}, status=status.HTTP_400_BAD_REQUEST)

        # Return a success response
        return Response({'message': 'Product redeemed successfully'}, status=status.HTTP_200_OK)
