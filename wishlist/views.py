from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Wishlist, Product
from .serializers import WishlistSerializer, ProductSerializer
from .supabase_client import supabase
from gotrue.errors import AuthApiError

# wishlist/views.py
from rest_framework import viewsets
from .models import Wishlist
from .serializers import WishlistSerializer
import logging

logger = logging.getLogger(__name__)

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def list(self, request, *args, **kwargs):
        logger.warning("Wishlist list hit by %s", request.user)
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in WishlistViewSet.list: %s", e)
            raise e

    def create(self, request, *args, **kwargs):
        logger.warning("Wishlist create hit by %s", request.user)
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in WishlistViewSet.create: %s", e)
            raise e


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        logger.warning("Product list hit by %s", request.user)
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in ProductViewSet.list: %s", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.warning("Product create hit by %s", request.user)
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in ProductViewSet.create: %s", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        logger.warning("Product retrieve hit by %s", request.user)
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in ProductViewSet.retrieve: %s", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        logger.warning("Product update hit by %s", request.user)
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in ProductViewSet.update: %s", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        logger.warning("Product delete hit by %s", request.user)
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in ProductViewSet.destroy: %s", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = supabase.auth.sign_up({"email": username, "password": password})
        print("Signup response type:", type(user))
        print("Signup response dir:", dir(user))
        print("Signup response repr:", repr(user))
        return Response({'message': f'User {username} signed up successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = supabase.auth.sign_in_with_password({"email": username, "password": password})
        print("Login response type:", type(user))
        print("Login response dir:", dir(user))
        print("Login response repr:", repr(user))
        # For now, just return the repr string to see the full response
        return Response({'login_response': repr(user)}, status=status.HTTP_200_OK)
    except AuthApiError as auth_error:
        if "Email not confirmed" in str(auth_error):
            return Response({'error': 'Email not confirmed'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': str(auth_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print("Exception traceback:", traceback_str)
        return Response({'error': str(e), 'traceback': traceback_str}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def invite_contributor(request, wishlist_id):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        wishlist = Wishlist.objects.get(id=wishlist_id)
    except Wishlist.DoesNotExist:
        return Response({'error': 'Wishlist not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        user_id_int = int(user_id)
    except ValueError:
        return Response({'error': 'user_id must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
    wishlist.contributors.add(user_id_int)
    wishlist.save()
    return Response({'message': f'User {user_id_int} added as contributor'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def sync_user(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username=email, defaults={'email': email})
    return Response({'id': user.id, 'created': created}, status=status.HTTP_200_OK)
